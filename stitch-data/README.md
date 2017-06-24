# Stitching the Spark Output into a CSV File Format 

This is the fourth section of instructions for setting up the Parallel Routing Analysis using OSRM and Postgres in Spark. In this section, I walk through stitching together the output of the Spark analysis into a CSV file format. To accomplish these tasks, I assume you have some familiarity with the command line and Python.

### Setup analysis environment

1. SSH into your EC2 instance running the Docker Postgres environment. If you're using Block Group or Block level data, you may need to spin up another instance with more memory, likely m4.10xlarge or m4.16xlarge.

2. Set up and install the Anaconda Python environment by following the instructions [here](https://www.continuum.io/downloads). You'll want to copy the link address to the 64-bit x86 installer for Python3 and running `wget <link address>` (e.g., `wget https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh`). Then run the bash command that Anaconda tells you to (e.g., `bash Anaconda3-4.4.0-Linux-x86_64.sh`) and follow and complete the prompts to install the software.

3. Setup AWS CLI configuration by exporting your keys to the environment as you did when setting up the Spark environment. 

   ```bash
   export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
   export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
   ```

4. Download the files produced from the Spark analysis using the AWS CLI, copying the `/path/to/bucket/output/folder` filepath from what you specified in the last line of get_estimates.py in the Spark process. This may take a few minutes.

   ```bash
   mkdir data
   mkdir output
   cd data
   aws s3 sync s3://path/to/bucket/output/folder .
   ```

### Stitch the Files Together

1. Copy the program stitch_files.py into the /home/ec2 folder and run it to convert the files to a single CSV and state based CSVs. Make sure to change the `geo` and `geo_length` field to the correct geography and geographic length identifier (11 for Census Tracts, 12 for Census Block Groups, 15 for Census Blocks).

   ```bash
   cd ../
   /home/ec2-user/anaconda3/bin/python stitch_files.py
   ```

2. Export your files to S3 to be used or shared.

   ```bash
   cd output
   aws s3 sync . s3://path/to/bucket/final/output/folder
   ```

3. That's it! Congratulations on creating a useful Census-level geographic road travel time dataset.