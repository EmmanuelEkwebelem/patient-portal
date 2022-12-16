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
Azure_TableNames = ['production_patients ', 'production_conditions', 'production_medications', 'sx_procedure','patient_conditions', 'patient_medications', 'patient_procedure']
print(Azure_TableNames)

# first step below is just creating a basic version of each of the tables,
# along with the primary keys and default values

####  CREATE TABLES  ####
table_production_patients  = """
create table if not exists production_patients  (
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

table_sx_procedure = """
create table if not exists sx_procedure (
    id int auto_increment,
    proc_cpt varchar(255) default null unique,
    proc_desc varchar(255) default null,
    PRIMARY KEY (id)
);
"""

table_production_conditions = """
create table if not exists conditions (
    id int auto_increment,
    icd10_code varchar(255) default null unique,
    icd10_desc varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""

table_production_medications = """
create table if not exists medications (
    id int auto_increment,
    med_ndc varchar(255) default null unique,
    med_human_name varchar(255) default null,
    med_is_dangerous varchar(255) default null,
    PRIMARY KEY (id)
); 
"""

table_patient_procedure = """
create table if not exists patient_procedure (
    id int auto_increment,
    mrn varchar(255) default null,
    proc_cpt varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (proc_cpt) REFERENCES sx_procedure(proc_cpt) ON DELETE CASCADE
); 
"""

table_patient_conditions = """
create table if not exists patient_conditions (
    id int auto_increment,
    mrn varchar(255) default null,
    icd10_code varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (icd10_code) REFERENCES conditions(icd10_code) ON DELETE CASCADE
); 
"""

table_patients_medications = """
create table if not exists patient_medications (
    id int auto_increment,
    mrn varchar(255) default null,
    med_ndc varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (med_ndc) REFERENCES medications(med_ndc) ON DELETE CASCADE
); 
"""

Azure_Database.execute(table_production_patients)
Azure_Database.execute(table_sx_procedure)
Azure_Database.execute(table_production_conditions)
Azure_Database.execute(table_production_medications)
Azure_Database.execute(table_patient_procedure)
Azure_Database.execute(table_patient_conditions)
Azure_Database.execute(table_patients_medications)


# get tables from db_azure
Azure_Tables = Azure_Database.table_names()