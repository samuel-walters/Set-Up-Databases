# MySQL

## Install MySQL on an AWS EC2 Instance

> 1. Create a new instance on AWS, and choose Ubuntu 20.04.
> 2. For the security group, allow your IP to SSH into the instance (on port 22), **and** allow port 3306 on your IP.
> 3. Select your key pair, and create the instance.
> 4. SSH into the instance, and run these commands:
``` bash
sudo apt update -y 
sudo apt install mysql-server -y
sudo systemctl start mysql.service
```
> 5. Type `sudo mysql`, and enter this line: `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'passwordhere';` and then type `exit`.
> 5. Run this script: `sudo mysql_secure_installation`. 
> 6. You can select `Y` for the following questions.

## Connecting to the MySQL Server through a SSH Tunnel

### MySQL Workbench
> 1. Install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
> 2. On MySQL Workbench, add a new connection with a configuration that resembles the details below:
![](https://i.imgur.com/mvSAQpu.png)

### Python Script

> 1. View the syntax for connecting to a MySQL server and running commands from a [Python Script here](connect_ssh_tunnel.py).

## Connecting to the MySQL Server Remotely

### Creating a MySQL User for Remote Access

> 1. Access the MySQL shell with `mysql -u root -p`. If that refuses to work, try `sudo mysql`.
> 2. Type in this command to create the user `samuel`: `CREATE USER 'samuel'@'%' IDENTIFIED BY 'passwordgoeshere';`.
> 3. Note: The `%` is unsafe here. It will allow the user in question to access the MySQL server remotely from anywhere, exposing the MySQL server to the risks of the remote user's password being lost or brute-forced. To make it more safe, you can specify a specific IP address from which the user can connect. The syntax looks like this: `'samuel'@'192.168.1.100'`.
> 4. Type in this command into the shell to update the user's permissions: `GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'samuel'@'%' WITH GRANT OPTION;`.
> 5. After running these two commands, run `FLUSH PRIVILEGES;`. 
> 6. Type `exit`, and then try connecting to the shell with `mysql -u samuel -p`. When prompted enter your password.

## Enable Remote Connection 

> 1. `sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf`.
> 2. For bind-address, fill it in as so: `bind-address            = 0.0.0.0`.
> 3. Restart the Ubuntu MySQL Server: `systemctl restart mysql.service`. 

### Connect Remotely with MySQL Workbench

> 1. Open a new connection. The details should look like the ones filled in below:

![](https://i.imgur.com/uqvlPPH.png)

### Connect Remotely with a Python Script

> 1. View the syntax for remotely running commands using a [Python Script here](remote_connect.py).

## Migrating a MySQL database between EC2 Instances

> 1. Run this command on the database you wish to transfer: `mysqldump -u root -p --opt [database_name] > [database_name].sql`.
> 2. If these instances use the same VPC, make sure the security group for the EC2 instance you are transferring the file to allows port 20 (the SSH port) for the private ip of the instance the file is being received from.  
> 3. The scp command may look like this if you use a private key to connect to your instance (note the private IP is being used here): `scp -i ~/.ssh/eng119.pem database_name.sql ubuntu@172.31.25.180:/home/ubuntu/`.
> 4. Once the file gets received, run this on your new instance: `mysql -u root -p existing_database_name_on_new_instance < /path/to/database_name.sql`. 


