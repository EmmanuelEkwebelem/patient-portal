import dbm
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

MySQL_Hostname = os.getenv('MySQL_Hostname')
MySQL_User = os.getenv('MySQL_User')
MySQL_Password = os.getenv('MySQL_Password')
MySQL_Database = os.getenv('MySQL_Database')

Database = create_engine(f'mysql+pymysql://{MySQL_User}:{MySQL_Password}@{MySQL_Hostname}:3306/{MySQL_Database}')
TableNames = Database.table_names

def drop_tables_limited(dbList, db_source):
    for table in dbList:
        if table.startswith('production') == False:
            db_source.exectute(f'Drop table {table}')
            print(f'{table} has been dropped')
        else:
            print(f'{table} has not been dropped')

def drop_tables_all(dbList, db_source):
    for table in dbList:
        db_source.execute(f'Drop table {table}')
        print(f'{table} has been dropped')
    else:
        print(f'{table} has not been dropped')


table_prod_patients = """
create table if not exists production_patients (
    id int auto_increment,
    mrn varchar(255) default null unique,
    first_name varchar(255) default null,
    last_name varchar(255) default null,
    zip_code varchar(255) default null,
    dob varchar(255) default null,
    age varchar(255) default null,
    gender varchar(255) default null,
    race varchar(255) default null,
	insurance_type varchar(255) default null,
    contact_mobile varchar(255) default null,
    contact_home varchar(255) default null,
    PRIMARY KEY (id)
); 
"""

table_prod_treatment_procedures = """
create table if not exists production_treatment_procedures (
    id int auto_increment,
    cpt_code varchar(255) default null unique,
    cpt_name varchar(255) default null,
    PRIMARY KEY (id)
);
"""

table_prod_medications = """
create table if not exists production_medications (
    id int auto_increment,
    med_ndc varchar(255) default null unique,
    med_human_name varchar(255) default null,
    med_is_dangerous varchar(255) default null,
    PRIMARY KEY (id)
); 
"""

table_prod_conditions = """
create table if not exists production_conditions (
    id int auto_increment,
    icd10_code varchar(255) default null unique,
    icd10_description varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""

table_prod_patients_medications = """
create table if not exists production_patient_medications (
    id int auto_increment,
    mrn varchar(255) default null,
    med_ndc varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES production_patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (med_ndc) REFERENCES production_medications(med_ndc) ON DELETE CASCADE
); 
"""

table_prod_patient_conditions = """
create table if not exists production_patient_conditions (
    id int auto_increment,
    mrn varchar(255) default null,
    icd10_code varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES production_patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (icd10_code) REFERENCES production_conditions(icd10_code) ON DELETE CASCADE
); 
"""

# execute the commands above to create tables
Database.execute(table_prod_patients)
Database.execute(table_prod_medications)
Database.execute(table_prod_conditions)
Database.execute(table_prod_patients_medications)
Database.execute(table_prod_patient_conditions)
Database.execute(table_prod_treatment_procedures)

Tables = Database.table_names()

# Reordering Tables
TableNames = ['production_patient_conditions', 'production_patient_medications', 'production_treatment_procedures', 'production_conditions', 'production_medications', 'production_patients',]
drop_tables_limited(TableNames, Database)