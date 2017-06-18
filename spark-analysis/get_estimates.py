from pyspark import SparkContext
from pyspark.sql import SparkSession
import psycopg2

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

