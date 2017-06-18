# Setting up the GIS Files and Postgres Environment

This is the second section of instructions for setting up the Parallel Routing Analysis using OSRM and Postgres in Spark. In this section, I walk through setting up the GIS file and Postgres environment. To accomplish these tasks, I assume you have some familiarity with Amazon Web Services, the command line, Docker, Postgres, and SQL.

1. First, spin up an instance on AWS with a decent amount of memory and at least 100GB of hard drive space (and potentially more if working with smaller files like blocks). I recommend a m4.2xlarge or bigger using the standard AWS Linux AMI. Make sure that the security settings allow others (0.0.0.0) to access port 5432 on the device, and make sure to set up a strong password in the next step to protect your Postgres instance from injection. Also make sure to write down the EC2 instance IP address for use in Apache Spark.

2. Run the following commands to install a Postgres instance on the machine using Docker and to enter the instance. Write down or copy your password somewhere for use in Spark.

   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo docker run -itd -p 5432:5432 --name my-postgis -e POSTGRES_PASSWORD=yourpassword mdillon/postgis
   sudo docker exec -it my-postgis bash
   ```

3. Within the server, run `setup_shapes.sh` by copying the file into the container and running `./setup_shapes.sh` or `bash setup_shapes.sh`. The default level is Census tracts `geog=tract`, but it will also work for the following: Census Block `geog=tabblock10`, Census Block Group `geog=bg`, and Census Public Use Microdata Area `geog=puma10`. Just replace the `geog=tract` statement with the correct `geog=` statement in the `download_shapes.sh` file. For larger geographies, it may take significantly more time, and you may want to reduce the parameter `3.0`, which indicates that all tracts within 3 decimal degrees are included (or wait!). This process takes about 20 minutes with Census tracts, and saves you hours or days in Spark.

