# Parallel Routing Analysis using OSRM and Postgres in Spark

This repository contains instructions and code for creating real driving time and distance calculations at scale, for data analysts who want to go beyond simple "as the crow flies" measures. It is split into four parts:

- Setting up the OSRM files (osrm-setup - **completed**) 
- Setting up the GIS files and Postgres environment (postgres-setup - **completed**) 
- Running the analysis to produce the estimates in Spark (spark-analysis - **completed**)
- Stitching the Spark output into a CSV file format (stitch-data - **completed**)

To use these tools, I expect you have some familiarity with Amazon Web Services, the command line, Docker, Postgres, SQL, Spark, and Python. For the data, go the pages site: https://ui-research.github.io/spark-osrm/.