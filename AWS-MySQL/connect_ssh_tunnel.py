from sshtunnel import SSHTunnelForwarder
import pymysql

remote_hostname = input("Please enter the remote hostname: ")
host_user = input("Please enter the username used to connect to your remote host: ")
# the path, for example, could be '~/.ssh/private_key.pem'.
private_key = input("Please enter the path to your private key: ")

user_input = input("Please enter your MySQL username: ")
password_input = input("Please enter the password for " + user_input + ": ")

def run_sql_command(sql_command, query=False):
    tunnel = SSHTunnelForwarder(
    (remote_hostname, 22),
    ssh_username=host_user,
    ssh_pkey=private_key,
    remote_bind_address = ('127.0.0.1', 3306)
    )

    tunnel.start()

    connection = pymysql.connect(
        host="127.0.0.1",
        user=user_input,
        password=password_input,
        db="database_here",
        port=tunnel.local_bind_port,
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_command)
                if query:
                    result = cursor.fetchall()
                    tunnel.close()
                    return result
                connection.commit()
            except Exception as mysql_error:
                print("MySQL Error for the command '" + sql_command + "' : " + str(mysql_error))
    tunnel.close()

run_sql_command(
    "CREATE TABLE testing_table(id int NOT NULL AUTO_INCREMENT, name VARCHAR(255), age INT, PRIMARY KEY (id));"
    )

run_sql_command(
   "INSERT INTO testing_table(name, age) VALUES ('Anson', 24), ('Shuvo', 27);"
   )

print(run_sql_command("SELECT * FROM testing_table;", query=True))
print(run_sql_command("SELECT * FROM testing_table WHERE name='shuvo';", query=True))