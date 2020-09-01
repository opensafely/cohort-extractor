"""
The EMIS data is accessed via Presto which is a distributed query engine which
runs over multiple backing data stores ("connectors" in Presto's parlance).
The production configuration uses the following connectors:

    hive for views
    delta-lake for underlying data
    mysql for config/metadata

For immediate convenience while testing we use the SQL Server connector (as we
already need an instance running for the TPP tests).
"""
import os
import time

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    NVARCHAR,
    Date,
    BigInteger,
)
from sqlalchemy import ForeignKey
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapper

from cohortextractor.mssql_utils import mssql_sqlalchemy_engine_from_url
from cohortextractor.presto_utils import wait_for_presto_to_be_ready

Base = declarative_base()
metadata = Base.metadata


def make_engine():
    engine = mssql_sqlalchemy_engine_from_url(
        os.environ["EMIS_DATASOURCE_DATABASE_URL"]
    )
    timeout = os.environ.get("CONNECTION_RETRY_TIMEOUT")
    timeout = float(timeout) if timeout else 60
    # Wait for the database to be ready if it isn't already
    start = time.time()
    while True:
        try:
            engine.connect()
            break
        except sqlalchemy.exc.DBAPIError:
            if time.time() - start < timeout:
                time.sleep(1)
            else:
                raise
    wait_for_presto_to_be_ready(
        os.environ["EMIS_DATABASE_URL"],
        # Presto will show active nodes in its `system.runtime.nodes` table but
        # then throw a "no nodes available" error if you try to execute a query
        # which needs to touch the MSSQL instance. So to properly confirm that
        # Presto is ready we need a query which forces it to connect to MSSQL,
        # but ideally one which doesn't depend on any particular configuration
        # having been done first. The below seems to do the trick.
        "SELECT 1 FROM sys.tables",
        timeout,
    )
    return engine


def make_session():
    engine = make_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


def make_database():
    Base.metadata.create_all(make_engine())


class Patient(Base):
    __tablename__ = "patient_view"

    registration_id = Column(Integer, primary_key=True)
    date_of_birth = Column(DateTime)
    gender = Column(Integer)
    registered_date = Column(DateTime)
    registration_end_date = Column(DateTime)
    rural_urban = Column(Integer)
    imd_rank = Column(Integer)
    msoa = Column(String)
    stp_code = Column(String)
    stp_name = Column(String)
    english_region_code = Column(String)
    english_region_name = Column(String)

    medications = relationship(
        "Medication", back_populates="patient", cascade="all, delete, delete-orphan"
    )
    observations = relationship(
        "Observation", back_populates="patient", cascade="all, delete, delete-orphan"
    )
    ICNARC = relationship(
        "ICNARC", back_populates="patient", cascade="all, delete, delete-orphan"
    )
    ONSDeath = relationship(
        "ONSDeaths", back_populates="patient", cascade="all, delete, delete-orphan"
    )
    CPNS = relationship(
        "CPNS", back_populates="patient", cascade="all, delete, delete-orphan"
    )


class Medication(Base):
    __tablename__ = "medication_view"

    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("patient_view.registration_id"))
    patient = relationship("Patient", back_populates="medications")
    snomed_concept_id = Column(BigInteger)
    effective_date = Column(DateTime)


class Observation(Base):
    __tablename__ = "observation_view"

    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("patient_view.registration_id"))
    patient = relationship("Patient", back_populates="observations")
    snomed_concept_id = Column(BigInteger)
    value_pq_1 = Column(Float)
    effective_date = Column(DateTime)


class ICNARC(Base):
    __tablename__ = "icnarc_view"

    icnarc_id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("patient_view.registration_id"))
    patient = relationship("Patient", back_populates="ICNARC")
    icuadmissiondatetime = Column(DateTime)
    originalicuadmissiondate = Column(Date)
    basicdays_respiratorysupport = Column(Integer)
    advanceddays_respiratorysupport = Column(Integer)
    ventilator = Column(Integer)


class ONSDeaths(Base):
    __tablename__ = "ons_view"

    # This column isn't in the actual database but SQLAlchemy gets a bit upset
    # if we don't give it a primary key
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("patient_view.registration_id"))
    patient = relationship("Patient", back_populates="ONSDeath")
    sex = Column(String)
    ageinyrs = Column(Integer)
    dod = Column(Date)
    icd10u = Column(String)
    icd10001 = Column(String)
    icd10002 = Column(String)
    icd10003 = Column(String)
    icd10004 = Column(String)
    icd10005 = Column(String)
    icd10006 = Column(String)
    icd10007 = Column(String)
    icd10008 = Column(String)
    icd10009 = Column(String)
    icd10010 = Column(String)
    icd10011 = Column(String)
    icd10012 = Column(String)
    icd10013 = Column(String)
    icd10014 = Column(String)
    icd10015 = Column(String)


class CPNS(Base):
    __tablename__ = "cpns_view"

    registration_id = Column(Integer, ForeignKey("patient_view.registration_id"))
    patient = relationship("Patient", back_populates="CPNS")
    id = Column(Integer, primary_key=True)
    # locationofdeath                                                 ITU
    # sex                                                               M
    # dateofadmission                                          2020-04-02
    # dateofswabbed                                            2020-04-02
    # dateofresult                                             2020-04-03
    # relativesaware                                                    Y
    # travelhistory                                                 False
    # regioncode                                                      Y62
    # regionname                                               North West
    # organisationcode                                                ABC
    # organisationname                                Test Hospital Trust
    # organisationtypelot                                        Hospital
    # regionapproved                                                 True
    # regionalapproveddate                                     2020-04-09
    # nationalapproved                                               True
    # nationalapproveddate                                     2020-04-09
    # preexistingcondition                                          False
    # age                                                              57
    dateofdeath = Column(Date)
    # snapdate                                                 2020-04-09
    # hadlearningdisability                                            NK
    # receivedtreatmentformentalhealth                                 NK
    # der_ethnic_category_description                                None
    # der_latest_sus_attendance_date_for_ethnicity                   None
    # der_source_dataset_for_ethnicty                                None
