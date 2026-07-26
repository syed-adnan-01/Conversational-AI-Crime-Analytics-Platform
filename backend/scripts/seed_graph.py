import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.session import SessionLocal
from app.database.generated_models import Casemaster, Accused, Victim

def generate_cypher():
    print("Generating Cypher Seed Script...")
    db = SessionLocal()
    
    try:
        cases = db.query(Casemaster).all()
        accused_list = db.query(Accused).all()
        victims_list = db.query(Victim).all()

        output_file = os.path.join(os.path.dirname(__file__), 'graph_seed.cypher')

        with open(output_file, 'w') as f:
            f.write("// Neo4j Cypher Seed Script\n")
            f.write("// Clear existing data\n")
            f.write("MATCH (n) DETACH DELETE n;\n\n")

            f.write("// Constraints\n")
            f.write("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Case) REQUIRE c.id IS UNIQUE;\n")
            f.write("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;\n\n")

            f.write("// Create Cases\n")
            for case in cases:
                f.write(f"MERGE (c:Case {{id: '{case.casemasterid}'}}) ")
                f.write(f"ON CREATE SET c.crimeno = '{case.crimeno}', c.caseno = '{case.caseno}', c.brieffacts = '{case.brieffacts[:50] if case.brieffacts else ''}';\n")
            f.write("\n")

            f.write("// Create Accused\n")
            for acc in accused_list:
                f.write(f"MERGE (p:Person {{id: 'A_{acc.accusedmasterid}'}}) ")
                f.write(f"ON CREATE SET p.name = '{acc.accusedname}', p.role = 'Accused';\n")
                f.write(f"MATCH (p:Person {{id: 'A_{acc.accusedmasterid}'}}), (c:Case {{id: '{acc.casemasterid}'}}) ")
                f.write("MERGE (p)-[:ACCUSED_IN]->(c);\n")
            f.write("\n")

            f.write("// Create Victims\n")
            for vic in victims_list:
                f.write(f"MERGE (p:Person {{id: 'V_{vic.victimmasterid}'}}) ")
                f.write(f"ON CREATE SET p.name = '{vic.victimname}', p.role = 'Victim';\n")
                f.write(f"MATCH (p:Person {{id: 'V_{vic.victimmasterid}'}}), (c:Case {{id: '{vic.casemasterid}'}}) ")
                f.write("MERGE (p)-[:VICTIM_IN]->(c);\n")
            f.write("\n")
            
            f.write("// Add some random relationships between Accused (e.g. KNOWS)\n")
            f.write("MATCH (a1:Person {role: 'Accused'}), (a2:Person {role: 'Accused'}) \n")
            f.write("WITH a1, a2, rand() AS r WHERE r > 0.99 AND a1.id <> a2.id\n")
            f.write("MERGE (a1)-[:KNOWS]->(a2);\n")

        print(f"Generated successfully at {output_file}")

    except Exception as e:
        print(f"Error generating Cypher: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_cypher()
