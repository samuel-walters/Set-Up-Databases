# MongoDB 

## Install MongoDB on an AWS EC2 Instance

> 1. Run these commands:
```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt update
sudo apt install mongodb-org -y
```
> 2. Run the following systemctl command to start the MongoDB service: `sudo systemctl start mongod.service`.
> 3. Check the status with `sudo systemctl status mongod`.
> 4. Enable the MongoDB service to start up at boot: `sudo systemctl enable mongod`.

## Create an Admin User for Security

> 1. Type `mongo`. Then type `use admin`. 
> 2. Create an admin user with this line, replacing the username and password as you see fit: `db.createUser({ user: "mongoadmin" , pwd: "mongoadmin", roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]})`. 
> 3. Type `exit`.
> 4. Type `sudo nano /etc/mongod.conf` and scroll down to the commented out security section.
> 5. Uncomment `security`, and add an "authorization: enabled" section under it which is indented by two spaces as shown below:
```
security:
  authorization: enabled
```
> 6. Restart the daemon so these changes come into effect: `sudo systemctl restart mongod`. 
> 7. Check it has restarted properly with this command: `sudo systemctl status mongod`.
> 8. Type `mongo -u mongoadmin -p --authenticationDatabase admin` to log in as the admin user. 

## Set Up Remote Access

Note: these are EC2 Instances on the same VPC. If your situation is different, use the public IPs of the instances instead of the private IPs.

> 1. The remote machine must have mongo shell installed.
> 2. For the security group, add port 27017 and, if the instances use the same VPC, allow it for the private IPS of both your EC2 instances. You allow it for the mongodb host so it can listen on port 27017, and you allow it for the remote host so it can connect to the server on this port as well.
> 3. Type `sudo lsof -i | grep mongo` on your instance hosting mongodb, and make sure it is listening to port 27017.
> 4. Type `sudo nano /etc/mongod.conf`, and by `bindIp`, enter a comma and then the private ip of your MongoDB server's private IP address. For example, it may look like this:
```
net:
  port: 27017
  bindIp: 127.0.0.1,172.31.28.240
```
> 5. Restart MongoDB to put these changes into effect: `sudo systemctl restart mongod`.
> 6. Connect from the remote host with this command, replacing username with the admin user you set up and the IP address with the MongoDB server's private IP: `mongo "mongodb://username@mongo_server_ip:27017"`. 