from pyspark import SparkContext
from pyspark.sql import SparkSession
import psycopg2
import json

sc = SparkContext
spark = SparkSession.builder.getOrCreate()

geo_ip = 'EC2 IP OF DATABASE HERE'
password = 'YOUR POSTGRES PASSWORD HERE'
geo_name = 'tract'
osrm_ip = '0.0.0.0'

# Get number of rows and calculate partitions
with psycopg2.connect("dbname=postgres user=postgres password={} host={} port=5432".format(password,geo_ip)) as conn:
	with conn.cursor() as cur:
		query = 'SELECT MAX(id) FROM {}_within'.format(geo_name)
		cur.execute(query)
		fetch_obj = cur.fetchone()
		num_rows = fetch_obj[0]
		num_parts = num_rows / 5000

# Read in data
data = spark.read.format('jdbc').options(url='jdbc:postgresql://{}:5432/postgres?user=postgres&password={}'.format(geo_ip,password), 
		dbtable='{}_within'.format(geo_name), driver="org.postgresql.Driver", partitionColumn="id", lowerBound=1, upperBound=num_rows, numPartitions=num_parts).load()

# Define analysis
def analysis(line):
	import requests
	import json
	url = 'http://0.0.0.0:5000/route/v1/driving/{},{};{},{}'
	r = requests.get(url.format(line[3],line[4],line[5],line[6])).text
	data = json.loads(r)
	distance = round(data["routes"][0]["distance"]/1000, 1)
	duration = round(data["routes"][0]["duration"]/60, 1)
	return [line[0],distance,duration]

# Run Spark job
data_rdd = data.rdd
results = data_rdd.map(analysis).collect()

# Write Data to File
with open('/mnt/results.json', 'wb') as f:
	json.dump(results, f)
