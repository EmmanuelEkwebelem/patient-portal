# Setup 

## Azure VM

1. Go to to to Google Gloud Console and login 

2. Open or create a project and create a new MySQL Instance 
- Search and select 'SQL' 
- On the top left select 'Create Instance' and select 'Choose MySQL'
- Create a unique 'instance ID'
- Create a password
- Select database version 8.0 or later
- Choose the production configuration
- View additional configureation options
- Change machine type to lightweight, 1vCPU, 3.75GB
- Ensure a public IP is select under connections
- Under connections, add a network (0.0.0.0/0)
- Create instance

3. Create a new database inside of that mysql instance called patient_portal
- Inside of new instance navigate to 'Databases' and select 'Create Database'
- Choose a unique name and create

4. Create .env files with 
- MySQL_Hostname = SQL IP Address
MySQL_User = "root"
MySQL_Password = Passwored created during "MySQL" instance creation
MySQL_Database = Database name

5. Creant and run .py files
- Create sql_table_creation.py and sql_dummy_data.py 
- Run sql_table_creation.py and sql_dummy_data.py 

6. View Database on MySQL Workbench