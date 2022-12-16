import dbm
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

MySQL_Azure_Hostname = os.getenv('MySQL_Azure_Hostname')
MySQL_Azure_User = os.getenv('MySQL_Azure_User')
MySQL_Azure_Password = os.getenv('MySQL_Azure_Password')
MySQL_Azure_Database = os.getenv('MySQL_Azure_Database')

Azure_Database = create_engine(f'mysql+pymysql://{MySQL_Azure_User}:{MySQL_Azure_Password}@{MySQL_Azure_Hostname}:3306/{MySQL_Azure_Database}')

Azure_TableNames = Azure_Database.table_names()
print(Azure_TableNames)

def droppingFunction_limited(AzureList, Azure_Source):
    for table in AzureList:
        if table.startswith('production_') == False:
            Azure_Source.execute(f'drop table {table}')
            print(f'dropped table {table}')
        else:
            print(f'kept table {table}')

def droppingFunction_all(AzureList, Azure_Source):
    for table in AzureList:
        Azure_Source.execute(f'drop table {table}')
        print(f'dropped table {table} succesfully!')
    else:
        print(f'kept table {table}')



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

table_prod_treatments_procedures = """
create table if not exists production_treatments_procedures (
    id int auto_increment,
    cpt varchar(255) default null unique,
    PRIMARY KEY (id)
); 
"""

# execute the commands above to create tables
Azure_Database.execute(table_prod_patients)
Azure_Database.execute(table_prod_medications)
Azure_Database.execute(table_prod_conditions)
Azure_Database.execute(table_prod_patients_medications)
Azure_Database.execute(table_prod_patient_conditions)
Azure_Database.execute(table_prod_treatments_procedures)



# show tables from databases
Azure_Tables = Azure_Database.table_names()

# reorder tables based on what will be the parent table vs. child table
Azure_TableNames = ['production_patient_conditions', 'production_patient_medications', 'production_medications', 'production_patients', 'production_conditions']

# delete everything
droppingFunction_all(Azure_TableNames, Azure_Database)