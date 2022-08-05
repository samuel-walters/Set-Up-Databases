import pymysql

user_sql = input("Please enter your MySQL username: ")
password_sql = input("Please enter your MySQL password: ")

def run_sql_command(sql_command, query=False):
    # Connect to the database
    connection = pymysql.connect(host='ec2-34-243-10-49.eu-west-1.compute.amazonaws.com',
                                user=user_sql,
                                password=password_sql,
                                database='database_here',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_command)
                if query:
                    result = cursor.fetchall()
                    return result
                connection.commit()
            except Exception as mysql_error:
                print("MySQL Error for the command '" + sql_command + "' : " + str(mysql_error))
    
run_sql_command(
    "CREATE TABLE movies(id int NOT NULL AUTO_INCREMENT, name VARCHAR(255), released DATE, PRIMARY KEY (id));"
    )

run_sql_command(
   "INSERT INTO movies(name, released) VALUES ('The Shining', '1980-11-07'), ('Doctor Sleep', '2019-10-31');"
   )

print(run_sql_command("SELECT * FROM movies;", query=True))
print(run_sql_command("SELECT * FROM movies WHERE released > '2000-01-01';", query=True))
    
