from typing import Optional
import datetime
import decimal

from sqlalchemy import Boolean, CHAR, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Act(Base):
    __tablename__ = 'act'
    __table_args__ = (
        PrimaryKeyConstraint('actcode', name='act_pkey'),
    )

    actcode: Mapped[str] = mapped_column(String(20), primary_key=True)
    actdescription: Mapped[Optional[str]] = mapped_column(String(255))
    shortname: Mapped[Optional[str]] = mapped_column(String(100))
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    section: Mapped[list['Section']] = relationship('Section', back_populates='act')
    crimeheadactsection: Mapped[list['Crimeheadactsection']] = relationship('Crimeheadactsection', back_populates='act')
    actsectionassociation: Mapped[list['Actsectionassociation']] = relationship('Actsectionassociation', back_populates='act')


class Casecategory(Base):
    __tablename__ = 'casecategory'
    __table_args__ = (
        PrimaryKeyConstraint('casecategoryid', name='casecategory_pkey'),
    )

    casecategoryid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lookupvalue: Mapped[str] = mapped_column(String(100), nullable=False)

    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='casecategory')


class Casestatusmaster(Base):
    __tablename__ = 'casestatusmaster'
    __table_args__ = (
        PrimaryKeyConstraint('casestatusid', name='casestatusmaster_pkey'),
    )

    casestatusid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    casestatusname: Mapped[str] = mapped_column(String(100), nullable=False)

    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='casestatusmaster')


class Castemaster(Base):
    __tablename__ = 'castemaster'
    __table_args__ = (
        PrimaryKeyConstraint('caste_master_id', name='castemaster_pkey'),
    )

    caste_master_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    caste_master_name: Mapped[str] = mapped_column(String(100), nullable=False)

    complainantdetails: Mapped[list['Complainantdetails']] = relationship('Complainantdetails', back_populates='castemaster')


class Crimehead(Base):
    __tablename__ = 'crimehead'
    __table_args__ = (
        PrimaryKeyConstraint('crimeheadid', name='crimehead_pkey'),
    )

    crimeheadid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crimegroupname: Mapped[str] = mapped_column(String(150), nullable=False)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    crimesubhead: Mapped[list['Crimesubhead']] = relationship('Crimesubhead', back_populates='crimehead')
    crimeheadactsection: Mapped[list['Crimeheadactsection']] = relationship('Crimeheadactsection', back_populates='crimehead')
    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='crimehead')


class Designation(Base):
    __tablename__ = 'designation'
    __table_args__ = (
        PrimaryKeyConstraint('designationid', name='designation_pkey'),
    )

    designationid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    designationname: Mapped[str] = mapped_column(String(100), nullable=False)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    sortorder: Mapped[Optional[int]] = mapped_column(Integer)

    employee: Mapped[list['Employee']] = relationship('Employee', back_populates='designation')


class Gravityoffence(Base):
    __tablename__ = 'gravityoffence'
    __table_args__ = (
        PrimaryKeyConstraint('gravityoffenceid', name='gravityoffence_pkey'),
    )

    gravityoffenceid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lookupvalue: Mapped[str] = mapped_column(String(100), nullable=False)

    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='gravityoffence')


class Occupationmaster(Base):
    __tablename__ = 'occupationmaster'
    __table_args__ = (
        PrimaryKeyConstraint('occupationid', name='occupationmaster_pkey'),
    )

    occupationid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    occupationname: Mapped[str] = mapped_column(String(100), nullable=False)

    complainantdetails: Mapped[list['Complainantdetails']] = relationship('Complainantdetails', back_populates='occupationmaster')


class Rank(Base):
    __tablename__ = 'rank'
    __table_args__ = (
        PrimaryKeyConstraint('rankid', name='rank_pkey'),
    )

    rankid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rankname: Mapped[str] = mapped_column(String(100), nullable=False)
    hierarchy: Mapped[Optional[int]] = mapped_column(Integer)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    employee: Mapped[list['Employee']] = relationship('Employee', back_populates='rank')


class Religionmaster(Base):
    __tablename__ = 'religionmaster'
    __table_args__ = (
        PrimaryKeyConstraint('religionid', name='religionmaster_pkey'),
    )

    religionid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    religionname: Mapped[str] = mapped_column(String(100), nullable=False)

    complainantdetails: Mapped[list['Complainantdetails']] = relationship('Complainantdetails', back_populates='religionmaster')


class State(Base):
    __tablename__ = 'state'
    __table_args__ = (
        PrimaryKeyConstraint('stateid', name='state_pkey'),
    )

    stateid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    statename: Mapped[str] = mapped_column(String(100), nullable=False)
    nationalityid: Mapped[Optional[int]] = mapped_column(Integer)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    district: Mapped[list['District']] = relationship('District', back_populates='state')
    court: Mapped[list['Court']] = relationship('Court', back_populates='state')
    unit: Mapped[list['Unit']] = relationship('Unit', back_populates='state')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='state')


class Unittype(Base):
    __tablename__ = 'unittype'
    __table_args__ = (
        PrimaryKeyConstraint('unittypeid', name='unittype_pkey'),
    )

    unittypeid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unittypename: Mapped[str] = mapped_column(String(100), nullable=False)
    citydiststate: Mapped[Optional[str]] = mapped_column(String(50))
    hierarchy: Mapped[Optional[int]] = mapped_column(Integer)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    unit: Mapped[list['Unit']] = relationship('Unit', back_populates='unittype')


class Crimesubhead(Base):
    __tablename__ = 'crimesubhead'
    __table_args__ = (
        ForeignKeyConstraint(['crimeheadid'], ['crimehead.crimeheadid'], name='fk_crimesubhead_crimehead'),
        PrimaryKeyConstraint('crimesubheadid', name='crimesubhead_pkey')
    )

    crimesubheadid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crimeheadid: Mapped[int] = mapped_column(Integer, nullable=False)
    crimeheadname: Mapped[str] = mapped_column(String(150), nullable=False)
    seqid: Mapped[Optional[int]] = mapped_column(Integer)

    crimehead: Mapped['Crimehead'] = relationship('Crimehead', back_populates='crimesubhead')
    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='crimesubhead')


class District(Base):
    __tablename__ = 'district'
    __table_args__ = (
        ForeignKeyConstraint(['stateid'], ['state.stateid'], name='fk_district_state'),
        PrimaryKeyConstraint('districtid', name='district_pkey')
    )

    districtid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    districtname: Mapped[str] = mapped_column(String(100), nullable=False)
    stateid: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    state: Mapped['State'] = relationship('State', back_populates='district')
    court: Mapped[list['Court']] = relationship('Court', back_populates='district')
    unit: Mapped[list['Unit']] = relationship('Unit', back_populates='district')
    employee: Mapped[list['Employee']] = relationship('Employee', back_populates='district')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='district')


class Section(Base):
    __tablename__ = 'section'
    __table_args__ = (
        ForeignKeyConstraint(['actcode'], ['act.actcode'], name='fk_section_act'),
        PrimaryKeyConstraint('sectioncode', name='section_pkey')
    )

    actcode: Mapped[str] = mapped_column(String(20), nullable=False)
    sectioncode: Mapped[str] = mapped_column(String(20), primary_key=True)
    sectiondescription: Mapped[Optional[str]] = mapped_column(String(255))
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    act: Mapped['Act'] = relationship('Act', back_populates='section')
    crimeheadactsection: Mapped[list['Crimeheadactsection']] = relationship('Crimeheadactsection', back_populates='section')
    actsectionassociation: Mapped[list['Actsectionassociation']] = relationship('Actsectionassociation', back_populates='section')


class Court(Base):
    __tablename__ = 'court'
    __table_args__ = (
        ForeignKeyConstraint(['districtid'], ['district.districtid'], name='fk_court_district'),
        ForeignKeyConstraint(['stateid'], ['state.stateid'], name='fk_court_state'),
        PrimaryKeyConstraint('courtid', name='court_pkey')
    )

    courtid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courtname: Mapped[str] = mapped_column(String(150), nullable=False)
    districtid: Mapped[int] = mapped_column(Integer, nullable=False)
    stateid: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    district: Mapped['District'] = relationship('District', back_populates='court')
    state: Mapped['State'] = relationship('State', back_populates='court')
    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='court')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='court')


class Crimeheadactsection(Base):
    __tablename__ = 'crimeheadactsection'
    __table_args__ = (
        ForeignKeyConstraint(['actcode'], ['act.actcode'], name='fk_chas_act'),
        ForeignKeyConstraint(['crimeheadid'], ['crimehead.crimeheadid'], name='fk_chas_crimehead'),
        ForeignKeyConstraint(['sectioncode'], ['section.sectioncode'], name='fk_chas_section'),
        PrimaryKeyConstraint('crimeheadid', 'actcode', 'sectioncode', name='crimeheadactsection_pkey')
    )

    crimeheadid: Mapped[int] = mapped_column(Integer, primary_key=True)
    actcode: Mapped[str] = mapped_column(String(20), primary_key=True)
    sectioncode: Mapped[str] = mapped_column(String(20), primary_key=True)

    act: Mapped['Act'] = relationship('Act', back_populates='crimeheadactsection')
    crimehead: Mapped['Crimehead'] = relationship('Crimehead', back_populates='crimeheadactsection')
    section: Mapped['Section'] = relationship('Section', back_populates='crimeheadactsection')


class Unit(Base):
    __tablename__ = 'unit'
    __table_args__ = (
        ForeignKeyConstraint(['districtid'], ['district.districtid'], name='fk_unit_district'),
        ForeignKeyConstraint(['parentunit'], ['unit.unitid'], name='fk_parent_unit'),
        ForeignKeyConstraint(['stateid'], ['state.stateid'], name='fk_unit_state'),
        ForeignKeyConstraint(['unittypeid'], ['unittype.unittypeid'], name='fk_unit_type'),
        PrimaryKeyConstraint('unitid', name='unit_pkey')
    )

    unitid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unitname: Mapped[str] = mapped_column(String(150), nullable=False)
    unittypeid: Mapped[int] = mapped_column(Integer, nullable=False)
    stateid: Mapped[int] = mapped_column(Integer, nullable=False)
    districtid: Mapped[int] = mapped_column(Integer, nullable=False)
    parentunit: Mapped[Optional[int]] = mapped_column(Integer)
    nationalityid: Mapped[Optional[int]] = mapped_column(Integer)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    district: Mapped['District'] = relationship('District', back_populates='unit')
    unit: Mapped[Optional['Unit']] = relationship('Unit', remote_side=[unitid], back_populates='unit_reverse')
    unit_reverse: Mapped[list['Unit']] = relationship('Unit', remote_side=[parentunit], back_populates='unit')
    state: Mapped['State'] = relationship('State', back_populates='unit')
    unittype: Mapped['Unittype'] = relationship('Unittype', back_populates='unit')
    employee: Mapped[list['Employee']] = relationship('Employee', back_populates='unit')
    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='unit')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='unit')


class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = (
        ForeignKeyConstraint(['designationid'], ['designation.designationid'], name='fk_employee_designation'),
        ForeignKeyConstraint(['districtid'], ['district.districtid'], name='fk_employee_district'),
        ForeignKeyConstraint(['rankid'], ['rank.rankid'], name='fk_employee_rank'),
        ForeignKeyConstraint(['unitid'], ['unit.unitid'], name='fk_employee_unit'),
        PrimaryKeyConstraint('employeeid', name='employee_pkey'),
        UniqueConstraint('kgid', name='employee_kgid_key')
    )

    employeeid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    districtid: Mapped[int] = mapped_column(Integer, nullable=False)
    unitid: Mapped[int] = mapped_column(Integer, nullable=False)
    rankid: Mapped[int] = mapped_column(Integer, nullable=False)
    designationid: Mapped[int] = mapped_column(Integer, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    kgid: Mapped[Optional[str]] = mapped_column(String(50))
    employeedob: Mapped[Optional[datetime.date]] = mapped_column(Date)
    genderid: Mapped[Optional[int]] = mapped_column(Integer)
    bloodgroupid: Mapped[Optional[int]] = mapped_column(Integer)
    physicallychallenged: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    appointmentdate: Mapped[Optional[datetime.date]] = mapped_column(Date)

    designation: Mapped['Designation'] = relationship('Designation', back_populates='employee')
    district: Mapped['District'] = relationship('District', back_populates='employee')
    rank: Mapped['Rank'] = relationship('Rank', back_populates='employee')
    unit: Mapped['Unit'] = relationship('Unit', back_populates='employee')
    casemaster: Mapped[list['Casemaster']] = relationship('Casemaster', back_populates='employee')
    chargesheetdetails: Mapped[list['Chargesheetdetails']] = relationship('Chargesheetdetails', back_populates='employee')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='employee')


class Casemaster(Base):
    __tablename__ = 'casemaster'
    __table_args__ = (
        ForeignKeyConstraint(['casecategoryid'], ['casecategory.casecategoryid'], name='fk_cm_category'),
        ForeignKeyConstraint(['casestatusid'], ['casestatusmaster.casestatusid'], name='fk_cm_status'),
        ForeignKeyConstraint(['courtid'], ['court.courtid'], name='fk_cm_court'),
        ForeignKeyConstraint(['crimemajorheadid'], ['crimehead.crimeheadid'], name='fk_cm_major'),
        ForeignKeyConstraint(['crimeminorheadid'], ['crimesubhead.crimesubheadid'], name='fk_cm_minor'),
        ForeignKeyConstraint(['gravityoffenceid'], ['gravityoffence.gravityoffenceid'], name='fk_cm_gravity'),
        ForeignKeyConstraint(['policepersonid'], ['employee.employeeid'], name='fk_cm_employee'),
        ForeignKeyConstraint(['policestationid'], ['unit.unitid'], name='fk_cm_unit'),
        PrimaryKeyConstraint('casemasterid', name='casemaster_pkey'),
        UniqueConstraint('crimeno', name='casemaster_crimeno_key')
    )

    casemasterid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crimeno: Mapped[str] = mapped_column(String(20), nullable=False)
    caseno: Mapped[str] = mapped_column(String(20), nullable=False)
    crimeregistereddate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    policepersonid: Mapped[int] = mapped_column(Integer, nullable=False)
    policestationid: Mapped[int] = mapped_column(Integer, nullable=False)
    casecategoryid: Mapped[int] = mapped_column(Integer, nullable=False)
    gravityoffenceid: Mapped[int] = mapped_column(Integer, nullable=False)
    crimemajorheadid: Mapped[int] = mapped_column(Integer, nullable=False)
    crimeminorheadid: Mapped[int] = mapped_column(Integer, nullable=False)
    casestatusid: Mapped[int] = mapped_column(Integer, nullable=False)
    courtid: Mapped[Optional[int]] = mapped_column(Integer)
    incidentfromdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    incidenttodate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inforeceivedpsdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(11, 8))
    brieffacts: Mapped[Optional[str]] = mapped_column(Text)

    casecategory: Mapped['Casecategory'] = relationship('Casecategory', back_populates='casemaster')
    casestatusmaster: Mapped['Casestatusmaster'] = relationship('Casestatusmaster', back_populates='casemaster')
    court: Mapped[Optional['Court']] = relationship('Court', back_populates='casemaster')
    crimehead: Mapped['Crimehead'] = relationship('Crimehead', back_populates='casemaster')
    crimesubhead: Mapped['Crimesubhead'] = relationship('Crimesubhead', back_populates='casemaster')
    gravityoffence: Mapped['Gravityoffence'] = relationship('Gravityoffence', back_populates='casemaster')
    employee: Mapped['Employee'] = relationship('Employee', back_populates='casemaster')
    unit: Mapped['Unit'] = relationship('Unit', back_populates='casemaster')
    accused: Mapped[list['Accused']] = relationship('Accused', back_populates='casemaster')
    actsectionassociation: Mapped[list['Actsectionassociation']] = relationship('Actsectionassociation', back_populates='casemaster')
    chargesheetdetails: Mapped[list['Chargesheetdetails']] = relationship('Chargesheetdetails', back_populates='casemaster')
    complainantdetails: Mapped[list['Complainantdetails']] = relationship('Complainantdetails', back_populates='casemaster')
    victim: Mapped[list['Victim']] = relationship('Victim', back_populates='casemaster')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='casemaster')


class Accused(Base):
    __tablename__ = 'accused'
    __table_args__ = (
        ForeignKeyConstraint(['casemasterid'], ['casemaster.casemasterid'], name='fk_accused_case'),
        PrimaryKeyConstraint('accusedmasterid', name='accused_pkey')
    )

    accusedmasterid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    casemasterid: Mapped[int] = mapped_column(Integer, nullable=False)
    accusedname: Mapped[str] = mapped_column(String(150), nullable=False)
    ageyear: Mapped[Optional[int]] = mapped_column(Integer)
    genderid: Mapped[Optional[int]] = mapped_column(Integer)
    personid: Mapped[Optional[str]] = mapped_column(String(20))

    casemaster: Mapped['Casemaster'] = relationship('Casemaster', back_populates='accused')
    arrestsurrender: Mapped[list['Arrestsurrender']] = relationship('Arrestsurrender', back_populates='accused')


class Actsectionassociation(Base):
    __tablename__ = 'actsectionassociation'
    __table_args__ = (
        ForeignKeyConstraint(['actid'], ['act.actcode'], name='fk_asa_act'),
        ForeignKeyConstraint(['casemasterid'], ['casemaster.casemasterid'], name='fk_asa_case'),
        ForeignKeyConstraint(['sectionid'], ['section.sectioncode'], name='fk_asa_section'),
        PrimaryKeyConstraint('casemasterid', 'actid', 'sectionid', name='actsectionassociation_pkey')
    )

    casemasterid: Mapped[int] = mapped_column(Integer, primary_key=True)
    actid: Mapped[str] = mapped_column(String(20), primary_key=True)
    sectionid: Mapped[str] = mapped_column(String(20), primary_key=True)
    actorderid: Mapped[Optional[int]] = mapped_column(Integer)
    sectionorderid: Mapped[Optional[int]] = mapped_column(Integer)

    act: Mapped['Act'] = relationship('Act', back_populates='actsectionassociation')
    casemaster: Mapped['Casemaster'] = relationship('Casemaster', back_populates='actsectionassociation')
    section: Mapped['Section'] = relationship('Section', back_populates='actsectionassociation')


class Chargesheetdetails(Base):
    __tablename__ = 'chargesheetdetails'
    __table_args__ = (
        ForeignKeyConstraint(['casemasterid'], ['casemaster.casemasterid'], name='fk_cs_case'),
        ForeignKeyConstraint(['policepersonid'], ['employee.employeeid'], name='fk_cs_employee'),
        PrimaryKeyConstraint('csid', name='chargesheetdetails_pkey')
    )

    csid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    casemasterid: Mapped[int] = mapped_column(Integer, nullable=False)
    csdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cstype: Mapped[Optional[str]] = mapped_column(CHAR(1))
    policepersonid: Mapped[Optional[int]] = mapped_column(Integer)

    casemaster: Mapped['Casemaster'] = relationship('Casemaster', back_populates='chargesheetdetails')
    employee: Mapped[Optional['Employee']] = relationship('Employee', back_populates='chargesheetdetails')


class Complainantdetails(Base):
    __tablename__ = 'complainantdetails'
    __table_args__ = (
        ForeignKeyConstraint(['casemasterid'], ['casemaster.casemasterid'], name='fk_complaint_case'),
        ForeignKeyConstraint(['casteid'], ['castemaster.caste_master_id'], name='fk_complaint_caste'),
        ForeignKeyConstraint(['occupationid'], ['occupationmaster.occupationid'], name='fk_complaint_occupation'),
        ForeignKeyConstraint(['religionid'], ['religionmaster.religionid'], name='fk_complaint_religion'),
        PrimaryKeyConstraint('complainantid', name='complainantdetails_pkey')
    )

    complainantid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    casemasterid: Mapped[int] = mapped_column(Integer, nullable=False)
    complainantname: Mapped[str] = mapped_column(String(150), nullable=False)
    ageyear: Mapped[Optional[int]] = mapped_column(Integer)
    occupationid: Mapped[Optional[int]] = mapped_column(Integer)
    religionid: Mapped[Optional[int]] = mapped_column(Integer)
    casteid: Mapped[Optional[int]] = mapped_column(Integer)
    genderid: Mapped[Optional[int]] = mapped_column(Integer)

    casemaster: Mapped['Casemaster'] = relationship('Casemaster', back_populates='complainantdetails')
    castemaster: Mapped[Optional['Castemaster']] = relationship('Castemaster', back_populates='complainantdetails')
    occupationmaster: Mapped[Optional['Occupationmaster']] = relationship('Occupationmaster', back_populates='complainantdetails')
    religionmaster: Mapped[Optional['Religionmaster']] = relationship('Religionmaster', back_populates='complainantdetails')


class Victim(Base):
    __tablename__ = 'victim'
    __table_args__ = (
        ForeignKeyConstraint(['casemasterid'], ['casemaster.casemasterid'], name='fk_victim_case'),
        PrimaryKeyConstraint('victimmasterid', name='victim_pkey')
    )

    victimmasterid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    casemasterid: Mapped[int] = mapped_column(Integer, nullable=False)
    victimname: Mapped[str] = mapped_column(String(150), nullable=False)
    ageyear: Mapped[Optional[int]] = mapped_column(Integer)
    genderid: Mapped[Optional[int]] = mapped_column(Integer)
    victimpolice: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    casemaster: Mapped['Casemaster'] = relationship('Casemaster', back_populates='victim')


class Arrestsurrender(Base):
    __tablename__ = 'arrestsurrender'
    __table_args__ = (
        ForeignKeyConstraint(['accusedmasterid'], ['accused.accusedmasterid'], name='fk_as_accused'),
        ForeignKeyConstraint(['arrestsurrenderdistrictid'], ['district.districtid'], name='fk_as_district'),
        ForeignKeyConstraint(['arrestsurrenderstateid'], ['state.stateid'], name='fk_as_state'),
        ForeignKeyConstraint(['casemasterid'], ['casemaster.casemasterid'], name='fk_as_case'),
        ForeignKeyConstraint(['courtid'], ['court.courtid'], name='fk_as_court'),
        ForeignKeyConstraint(['ioid'], ['employee.employeeid'], name='fk_as_io'),
        ForeignKeyConstraint(['policestationid'], ['unit.unitid'], name='fk_as_unit'),
        PrimaryKeyConstraint('arrestsurrenderid', name='arrestsurrender_pkey')
    )

    arrestsurrenderid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    casemasterid: Mapped[int] = mapped_column(Integer, nullable=False)
    arrestsurrendertypeid: Mapped[Optional[int]] = mapped_column(Integer)
    arrestsurrenderdate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    arrestsurrenderstateid: Mapped[Optional[int]] = mapped_column(Integer)
    arrestsurrenderdistrictid: Mapped[Optional[int]] = mapped_column(Integer)
    policestationid: Mapped[Optional[int]] = mapped_column(Integer)
    ioid: Mapped[Optional[int]] = mapped_column(Integer)
    courtid: Mapped[Optional[int]] = mapped_column(Integer)
    accusedmasterid: Mapped[Optional[int]] = mapped_column(Integer)
    isaccused: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    iscomplainantaccused: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    accused: Mapped[Optional['Accused']] = relationship('Accused', back_populates='arrestsurrender')
    district: Mapped[Optional['District']] = relationship('District', back_populates='arrestsurrender')
    state: Mapped[Optional['State']] = relationship('State', back_populates='arrestsurrender')
    casemaster: Mapped['Casemaster'] = relationship('Casemaster', back_populates='arrestsurrender')
    court: Mapped[Optional['Court']] = relationship('Court', back_populates='arrestsurrender')
    employee: Mapped[Optional['Employee']] = relationship('Employee', back_populates='arrestsurrender')
    unit: Mapped[Optional['Unit']] = relationship('Unit', back_populates='arrestsurrender')
