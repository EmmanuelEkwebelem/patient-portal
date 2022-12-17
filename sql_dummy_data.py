import dbm
import pandas
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from faker import Faker 
import uuid
import random

load_dotenv()

MySQL_Hostname = os.getenv('MySQL_Hostname')
MySQL_User = os.getenv('MySQL_User')
MySQL_Password = os.getenv('MySQL_Password')
MySQL_Database = os.getenv('MySQL_Database')

Database = create_engine(f'mysql+pymysql://{MySQL_User}:{MySQL_Password}@{MySQL_Hostname}:3306/{MySQL_Database}')

print(Database.table_names())

fake = Faker()

fake_patients = [
    {
        'mrn': str('AE' + str(random.randint(11111, 99999))),
        'first_name':fake.first_name(),
        'last_name':fake.last_name(),
        'zip_code':str(str(random.randint(100, 999)) + '-' + str(random.randint(10, 99))),
        'dob':(fake.date_between(start_date='-90y', end_date='-25y')).strftime('%m/%d/%Y'),
        'gender': fake.random_element(elements=('Male', 'Female', 'Other')),
        'race': fake.random_element(elements=('Black', 'Asian', 'White', 'Hispanic', 'Other')),
        'insurance_type': fake.random_element(elements=('Medicare', 'Medicaid', 'Private')),
        'contact_mobile': str(str(random.randint(100, 999)) + '-' + str(random.randint(100, 999)) + '-' + str(random.randint(1000, 9999))),
        'contact_home': fake.phone_number()
    } for x in range(50)]

df_fake_patients = pandas.DataFrame(fake_patients)
df_fake_patients = df_fake_patients.drop_duplicates(subset=['mrn'])


# Loading ICD10 Codes
icd10codes = pandas.read_csv('https://raw.githubusercontent.com/Bobrovskiy/ICD-10-CSV/master/2020/diagnosis.csv')
list(icd10codes.columns)
icd10codesShort = icd10codes[['CodeWithSeparator', 'ShortDescription']]
icd10codesShort_1k = icd10codesShort.sample(n=1000, random_state=1)
icd10codesShort_1k = icd10codesShort_1k.drop_duplicates(subset=['CodeWithSeparator'], keep='first')

# Loading NDC Codes
ndc_codes = pandas.read_csv('https://raw.githubusercontent.com/hantswilliams/FDA_NDC_CODES/main/NDC_2022_product.csv')
ndc_codes_1k = ndc_codes.sample(n=1000, random_state=1)
ndc_codes_1k = ndc_codes_1k.drop_duplicates(subset=['PRODUCTNDC'], keep='first')

# Loading CPT Codes
cptcodes = pandas.read_csv('https://gist.githubusercontent.com/lieldulev/439793dc3c5a6613b661c33d71fdd185/raw/25c3abcc5c24e640a0a5da1ee04198a824bf58fa/cpt4.csv')
list(cptcodes.columns)
cptcodesShort = cptcodes[['com.medigy.persist.reference.type.clincial.CPT.code', 'label']]
cptcodesShort_1k = cptcodesShort.sample(n=1000, random_state=1)
cptcodesShort_1k = cptcodesShort_1k.drop_duplicates(subset=['com.medigy.persist.reference.type.clincial.CPT.code'], keep='first')

insertQuery = "INSERT INTO production_patients (mrn, first_name, last_name, zip_code, dob, gender, race, insurance_type, contact_mobile, contact_home) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
for index, row in df_fake_patients.iterrows():
    Database.execute(insertQuery, (row['mrn'], row['first_name'], row['last_name'], row['zip_code'], row['dob'], row['gender'], row['race'], row['insurance_type'], row['contact_mobile'], row['contact_home']))
    print("inserted row: ", index)
Dataframe = pandas.read_sql_query("SELECT * FROM production_patients", Database)

insertQuery = "INSERT INTO production_treatment_procedures (cpt_code, cpt_name) VALUES (%s, %s)"

startingRow = 0
for index, row in cptcodesShort_1k.iterrows():
    startingRow += 1
    Database.execute(insertQuery, (row['com.medigy.persist.reference.type.clincial.CPT.code'], row['label']))
    print("inserted row: ", index)
    if startingRow == 100:
        break
Dataframe = pandas.read_sql_query("SELECT * FROM production_treatment_procedures", Database)

insertQuery = "INSERT INTO production_conditions (icd10_code, icd10_description) VALUES (%s, %s)"
startingRow = 0
for index, row in icd10codesShort_1k.iterrows():
    startingRow += 1
    Database.execute(insertQuery, (row['CodeWithSeparator'], row['ShortDescription']))
    print('inserted row Database: ', index)
    if startingRow == 100:
        break
Dataframe = pandas.read_sql_query("SELECT * FROM production_conditions", Database)

insertQuery = "INSERT INTO production_medications (med_ndc, med_human_name) VALUES (%s, %s)"
medRowCount = 0
for index, row in ndc_codes_1k.iterrows():
    medRowCount += 1
    Database.execute(insertQuery, (row['PRODUCTNDC'], row['NONPROPRIETARYNAME']))
    print('inserted row: ', index)
    if medRowCount == 100:
        break
Dataframe = pandas.read_sql_query("SELECT * FROM production_medications", Database)

df_conditions = pandas.read_sql_query('SELECT icd10_code FROM production_conditions', Database)
df_patients = pandas.read_sql_query('SELECT mrn FROM production_patients', Database)

df_patient_conditions = pandas.DataFrame(columns=['mrn', 'icd10_code'])
for index, row in df_patients.iterrows():
    numConditions = random.randint(1, 5)
    df_conditions_sample = df_conditions.sample(n=numConditions)
    df_conditions_sample['mrn'] = row['mrn']
    df_patient_conditions = df_patient_conditions.append(df_conditions_sample)
print(df_patient_conditions.head(10))

insertQuery = "INSERT INTO production_patient_conditions (mrn, icd10_code) VALUES (%s, %s)"
for index, row in df_patient_conditions.iterrows():
    Database.execute(insertQuery, (row['mrn'], row['icd10_code']))
    print('inserted row: ', index)

df_medications = pandas.read_sql_query("SELECT med_ndc FROM production_medications", Database) 
df_patients = pandas.read_sql_query("SELECT mrn FROM production_patients", Database)

df_patient_medications = pandas.DataFrame(columns=['mrn', 'med_ndc'])
for index, row in df_patients.iterrows():
    numMedications = random.randint(1, 5)
    df_medications_sample = df_medications.sample(n=numMedications)
    df_medications_sample['mrn'] = row['mrn']
    df_patient_medications = df_patient_medications.append(df_medications_sample)
print(df_patient_medications.head(10))

insertQuery = 'INSERT INTO production_patient_medications (mrn, med_ndc) VALUES (%s, %s)'
for index, row in df_patient_medications.iterrows():
    Database.execute(insertQuery, (row['mrn'], row['med_ndc']))
    print('inserted row: ', index)