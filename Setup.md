# Setup 

## Azure VM

1. Go to to to Azure Dashboard, select Virtual Machines, and select 'Create'

2. Fillout the VM information using the information below 
- Subscription: Azure for Students
- Virtual Machine Name: MySQL
- Region: (US) EAST US
- Availability Zone: Zones 1
- Image: Ubuntu Server 20.04 LTS -x64 Gen2
- Size: Standard_D2s_v3 - 2 vcpus, 8 GiB Memory
- Public Inbound Ports: Allow Selected Ports
- Select Inbout Ports: HTTP (80), HTTPS (433), SSH (22)
- Review and Create 


## Enable MySQL traffic

1. In order to allow MySQL traffic. Return back to to Azure Dashboard, select Virtual Machines, and select MySQL virtual machine 

2. Go to 'Networking', 'Inbound port rules' and then 'Add inbound port rule'
- Select 'MYSQL' for Service
- Change priority to 100
- Click Add 

3. Go to Overview and restart the MySQL VM from 


## Connect 

1. Open CMD Terinal 

2. SSH In: ssh -i <private key path> UserAdmin@4.236.187.210


## Set up OS image

1. Update OS command: sudo apt-get update

2. Install mysql command: sudo apt install mysql-server mysql-client

3. Install python: sudo apt-get install python3-dev default-libmysqlclient-dev

4. Login to mysql command: sudo mysql


## Create a User

1. Create a new user using the following command: CREATE USER 'newuser'@'%' IDENTIFIED BY 'password';
- This will create a new user called 'newuser' with the password 'password'. 

2. Next, you should grant the new user all privileges using the following command: GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'%' WITH GRANT OPTION;

3. Next, log out of the MySQL shell using the following command: exit

4. Log back into the MySQL shell with your new user account using the following command: mysql -u newuser -p


## Configure MySQL

1. Once your configuration is complete, you can exit the MySQL shell using the following command: exit

2. Next, you should bind the MySQL server to the public IP address. To do this, you need to edit the MySQL configuration file using the following command: sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

3. You should change the bind address from 127.0.0.0 to 0.0.0.0 and save the file and exit the editor

4. Finally, you should restart the MySQL server using the following command: sudo service mysql restart


## Load A DateSet in MySQL through mysql.py 

1. Keep VM Open/Running mysql in background

2. Open CMD Terinal (outside of VM)

3. Install: pip install python-dotenv, pip install pymysql, pip install mysql-connector-python, pip3 install Flask-SQLAlchemy, pip install pandas, pip install os

4. Open the mysql.py file 

5. Change mysql_Inputs: 
- mysql_host = VM IP Address
- mysql_user = mysql username
- mysql_password = mysql password
- mysql_data = created dataset
- query = 'select * from db1.created table;'

6. Run the sql_dummy_data.py and sql_table_creation.py files 

