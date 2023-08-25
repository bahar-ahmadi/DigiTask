import requests
import json

#!docker-compose up -d mysql mssql
#!docker-compose up -d zookeeper broker schema-registry connect

config = {
  "connector.class": "io.debezium.connector.mysql.MySqlConnector",
  "tasks.max": "1",
  "database.hostname": "mysql",
  "database.port": "3306",
  "database.user": "root",
  "database.password": "root",  
  "database.server.id": "184054",
  "database.server.name": "dbserver1",
  "database.whitelist": "testdb",
  "database.history.kafka.bootstrap.servers": "broker:29092",
  "database.history.kafka.topic": "schema-changes.testdb" 
}

requests.post('http://localhost:8083/connectors', 
              data=json.dumps(config), 
              headers={'Content-Type': 'application/json'})
              
config = {
  "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
  "connection.url": "jdbc:sqlserver://mssql:1433;databaseName=testdb",
  "connection.user": "sa",
  "connection.password": "YourStrong@Passw0rd",
  "topics": "server1.testdb.products",
  "auto.create": "true",
  "auto.evolve": "true",
  "insert.mode": "upsert",
  "pk.mode": "record_value",
  "pk.fields": "id",
  "transforms": "unwrap",
  "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
}

requests.post('http://localhost:8083/connectors', 
              data=json.dumps(config),
              headers={'Content-Type': 'application/json'}) 

print('MySQL and SQL Server CDC integration setup complete!')