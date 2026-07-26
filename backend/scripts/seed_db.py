import os
import sys
from datetime import datetime, timedelta
import random
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.session import SessionLocal, engine
from app.database.generated_models import (
    Casemaster, Victim, Accused, Employee, 
    Crimehead, Crimesubhead, Casestatusmaster,
    Designation, Casecategory, Gravityoffence
)

fake = Faker('en_IN')

CRIME_TYPES = [
    "Murder", "Cyber Crime", "Kidnapping", "Drug Trafficking",
    "Human Trafficking", "Robbery", "Theft", "Financial Fraud",
    "Domestic Violence", "Missing Persons", "Terror Investigation", "Sexual Assault"
]

def seed_db():
    print("Starting DB Seed...")
    db: Session = SessionLocal()
    
    try:
        print("Clearing old data...")
        db.execute(text("TRUNCATE TABLE accused CASCADE"))
        db.execute(text("TRUNCATE TABLE victim CASCADE"))
        db.execute(text("TRUNCATE TABLE casemaster CASCADE"))
        db.execute(text("TRUNCATE TABLE employee CASCADE"))
        db.execute(text("TRUNCATE TABLE designation CASCADE"))
        db.execute(text("TRUNCATE TABLE crimehead CASCADE"))
        db.commit()

        print("Seeding lookups...")
        designations = ["Inspector", "SP", "DSP", "Commissioner", "Constable", "Cyber Cell", "Forensic Officer"]
        designation_map = {}
        for idx, d_name in enumerate(designations, 1):
            desg = Designation(designationid=idx, designationname=d_name, active=True)
            db.add(desg)
            designation_map[d_name] = idx
        db.commit()

        employees = []
        for i in range(1, 101):
            emp = Employee(
                employeeid=i,
                firstname=fake.name(),
                rankid=1,
                designationid=random.choice(list(designation_map.values())),
                districtid=1,
                unitid=1
            )
            db.add(emp)
            employees.append(emp)
        db.commit()

        crime_head_map = {}
        for idx, crime_type in enumerate(CRIME_TYPES, 1):
            ch = Crimehead(crimeheadid=idx, crimegroupname=crime_type, active=True)
            db.add(ch)
            csh = Crimesubhead(crimesubheadid=idx, crimeheadid=idx, crimeheadname=crime_type)
            db.add(csh)
            crime_head_map[crime_type] = idx
        db.commit()

        print("Seeding 300 FIRs (Casemaster)...")
        cases = []
        for i in range(1, 301):
            crime_type = random.choice(CRIME_TYPES)
            reg_date = fake.date_time_between(start_date='-1y', end_date='now').date()
            
            case = Casemaster(
                crimeno=f"FIR-{reg_date.year}-{str(i).zfill(5)}",
                caseno=f"CASE-{reg_date.year}-{str(i).zfill(5)}",
                crimeregistereddate=reg_date,
                policepersonid=random.choice(employees).employeeid,
                policestationid=1,
                casecategoryid=1,
                gravityoffenceid=1,
                crimemajorheadid=crime_head_map[crime_type],
                crimeminorheadid=crime_head_map[crime_type],
                casestatusid=1,
                brieffacts=fake.text(max_nb_chars=500),
                latitude=float(fake.latitude()),
                longitude=float(fake.longitude())
            )
            db.add(case)
            cases.append(case)
            
        db.commit()
        
        print("Seeding Suspects (Accused) and Victims...")
        for case in cases:
            # Suspects (Accused)
            for _ in range(random.randint(1, 4)):
                accused = Accused(
                    casemasterid=case.casemasterid,
                    accusedname=fake.name(),
                    ageyear=random.randint(18, 65),
                    genderid=random.choice([1, 2])
                )
                db.add(accused)
            
            # Victims
            for _ in range(random.randint(1, 3)):
                victim = Victim(
                    casemasterid=case.casemasterid,
                    victimname=fake.name(),
                    ageyear=random.randint(10, 80),
                    genderid=random.choice([1, 2])
                )
                db.add(victim)

        db.commit()
        print(f"Database seeded successfully! (Seeded {len(cases)} cases, {len(employees)} employees)")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
