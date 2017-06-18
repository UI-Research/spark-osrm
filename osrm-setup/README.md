# Setting up the OSRM Files

This is the first section of instructions for setting up the Parallel Routing Analysis using OSRM and Postgres in Spark. In this section, I walk through setting up the OSRM files. To accomplish these tasks, I assume you have some familiarity with Amazon Web Services, the command line, and Docker.

1. Start up a large server from the Ubuntu Server AMI Amazon provides with plenty of cores and a decent amount of memory, and be sure to provision at least 100GB of hard drive space. You probably won't need more than 32GB Memory, but the more cores available, the faster this process will go. I recommend an m4.10xlarge or m4.16xlarge on the spot market to maximize processing power and reduce costs. The typical Amazon Linux AMI as default is fine.

2. Once your instance starts up and you SSH in, run the setup-ubuntu.sh script. You may need to issue the command `chmod +x setup-ubuntu.sh` before running to make it executable. You can run the script by typing `./setup-ubuntu.sh` or `bash setup-ubuntu.sh`.

3. Extract the data from the PBF file with the following code. This could take an hour or two.

   ```bash
   osrm-extract -p /osrm-backend/profiles/car.lua /north-america-latest.osm.pbf
   ```

4. Contract the data to easily loaded route form with the following code. This could take an hour or two.

   ```bash
   osrm-contract /north-america-latest.osrm
   ```

5. Test the files you've created. To do so, run `osrm-routed /north-america-latest.osrm`, and wait until the script notifies you it's loaded the names and is ready to accept requests, which should take a minute or two. Now, open up port 5000 to your IP in the security settings for your instance in the AWS Console, note the AWS EC2 IP for the instance, and navigate to the following site in your browser. It should return data in JSON immediately - if it doesn't, you may have done something incorrectly in the previous steps.

   ```html
   http://ec2-your-ec2-instance-ip:5000/route/v1/driving/-122.4107866,37.776945;-122.4297977,37.7857002
   ```

6. You should now have approximately 25 files with various file sizes that were created from this procedure. To use these in Spark, you'll need to upload the files to AWS S3. To do so, you'll need your AWS access key and secret key and an empty S3 bucket setup, and run the following code. In the S3 bucket, create a folder called "osrm-data".

   ```bash
   export AWS_ACCESS_KEY_ID=YOUR ACCESS KEY
   export AWS_SECRET_ACCESS_KEY=YOUR SECRET KEY
   mkdir /datatransfer
   mv /north-america-latest.osrm* /datatransfer/
   cd /datatransfer
   aws s3 sync . s3://<YOUR S3 BUCKET NAME>/osrm-data
   ```
