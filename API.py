from flask import Flask ,render_template, request , jsonify
import csv
from flask_mysqldb import MySQL
from flask_restful import Resource , Api , reqparse
import pyodbc


app = Flask(__name__)
api = Api(app)


#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['database'] = 'SampleDB'
mysql = MySQL(app)

#sql connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;uid=%s;pwd=%s' % ('.', 'sa', 'YourStrong@Passw0rd') , autocommit= True)



#PUT /mysql/db/{db-name}
@app.route("/mysql/db/<dbname>", methods=["PUT"])
def Create_Mysql_DB(dbname):
    cursor = mysql.connection.cursor()
    query = "CREATE DATABASE IF NOT EXISTS {}".format(dbname)
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()
    return "Database Created!"




#POST /mysql/db/{db-name}/tables/{table-name}
@app.route('/mysql/db/<db_name>/tables/<table_name>', methods=['POST'])  
def create_table( db_name,table_name):
  cursor = mysql.connection.cursor()
  with open('data/categories.csv' , encoding="utf8") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    schema = [f"{col} VARCHAR(255)" for col in header]
    cursor.execute(f'USE {db_name}')
    create_query = f"CREATE TABLE {table_name} ({', '.join(schema)})"  
    cursor.execute(create_query)
  mysql.connection.commit()
  cursor.close()
  return jsonify(message="Table created")



#PUT /mysql/db/{db-name}/tables/{table-name}/data`
@app.route('/mysql/db/<db_name>/tables/<table_name>/data', methods=['PUT'])
def insert_data(db_name, table_name):
  cursor = mysql.connection.cursor()
  # To Read CSV file 
  with open('data/categories.csv' , encoding="utf8" ) as file:
    csv_reader = csv.reader(file)
    # Ignore header row
    next(csv_reader)
    cursor.execute(f'USE {db_name}')
    # Insert rows
    for row in csv_reader:
      insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
      cursor.execute(insert_query, row)
  mysql.connection.commit() 
  cursor.close()
  return jsonify(message="Data inserted")



#PUT /mssql/db/{db-name}
@app.route("/mssql/db/<dbname>", methods=["PUT"])
def Create_mssql_DB(dbname):
    cursor = conn.cursor()
    query = "CREATE DATABASE {} ".format(dbname)
    cursor.execute(query)
    cursor.close()
    return "mssql Database Created!"


#POST /mssql/db/{db-name}/tables/{table-name}
@app.route('/mssql/db/<db_name>/tables/<table_name>', methods=['POST'])  
def create_table_mssql( db_name,table_name):
  cursor = conn.cursor()
  with open('data/categories.csv' , encoding="utf8") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    schema = [f"{col} VARCHAR(255)" for col in header]
    cursor.execute(f'USE {db_name}')
    create_query = f"CREATE TABLE {table_name} ({', '.join(schema)})"  
    cursor.execute(create_query)
  cursor.commit()
  cursor.close()
  return jsonify(message="mssql Table created")



if __name__ == "__main__":
    app.run()