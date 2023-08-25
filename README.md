# Digikala BI | Keeping an ODS Using Kafka

At Digikala BI, we have an operational data store (ODS) on SQL Server which is a live replica of Digikala's operational MySQL databases. We use Apache Kafka to stream the changes from the source MySQL servers and sink them down into SQL Server's ODS.

In this assignment, we're going to imitate that procedure.

You're going to set up Kafka and Kafka Connect, a source MySQL database, and a SQL Server as the downstream sink database. You'll be inserting mock data into the source database, and using Kafka Connect connectors, you'll create a replica of the source database in the destination db.

## Tasks

1. Create a docker-compose file that spins up a single-node Apache Kafka ecosystem containing a Kafka broker and a Kafka Connect service, and any other services necessary for Kafka to operate. You could simply use `landoop/fast-data-dev` image or you could go all the way and bring up a stack using Confluent's or Bitnami's images. Whatever you do, remember that *"simplicity is the ultimate sophistication".*

2. Add two other services called `mysql` and `mssql` to the docker-compose file for bringing up a MySQL and a Microsoft SQL Server database. Again, keep the configuration as simple as possible.

3. Develop an API in python with the following endpoints:

    * `PUT /mysql/db/{db-name}`
    
        Which creates a database in the source MySQL under the name `db-name`.
    
    * `POST /mysql/db/{db-name}/tables/{table-name}`
    
        Which creates the source table `table-name` with the appropriate schema for inserting the mock data from the accompanying CSV files. How you choose to get the schema using the API is up to you; you could infer the data-types automatically, you could get them from the request payload, or you could hard-code them. Proceed however you see best.

    * `PUT /mysql/db/{db-name}/tables/{table-name}/data`
        
        Which collects the data from the request payload and inserts the corresponding rows to the MySQL tables.

    * `PUT /mssql/db/{db-name}`

        Similar to the first endpoint for MySQL Server.

    * `POST /mssql/db/{db-name}/tables/{table-name}`
    
        Similar to the MySQL endpoint, for setting up the sink tables.

    Include the `Dockerfile` for building your own python API. You could start from any image you see fit, just make sure your image can be rebuilt by us (i.e. the base image or any other requirements are publicly available).
    
    Add the necessary configs for its deployment to the `docker-compose.yml` file. Be sure to expose your API port as well.

4. Create a jupyter-notebook for your solution. In the notebook, use your own APIs and those of Kafka Connect to create the source and destination databases and tables (use the CSV file-names for the source tables), and to submit two connectors (in whatever order you see fit): a `Debezium MySQL Source Connector` for capturing the changes from the MySQL db, and a `JDBC Sink Connector` for unwrapping the messages and sinking them down to the destination SQL Server.

The end result should be so that the data on the SQL Server tables are identical to the those on MySQL, and any changes made to the data on the source tables will also take effect on the destination tables.

Be sure to include any specific instructions required for testing out your solution.

Submit your solution as a branch to this repo, and email the local repository to us by at by most 7 days after receiving the task. If you have any questions in the meantime, feel free to reach us at [artin.zamani@digikala.com](mailto:artin.zamani@digikala.com) or [m.bolhasani@digikala.com](mailto:m.bolhasani@digikala.com). We'll be sure to respond ASAP.

Good luck.
