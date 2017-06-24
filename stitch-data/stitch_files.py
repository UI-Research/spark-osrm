import pandas as pd
import numpy as np
import glob
import csv
import json

print("Converting to CSV")
print("")
geo = 'tract'
geo_length = 11
filenames = glob.glob('/home/ec2-user/data/part-*')
with open('/home/ec2-user/output/{}_drive_times.csv'.format(geo), 'w') as f:
	writer = csv.writer(f)
	writer.writerow(['from_{}'.format(geo),'to_{}'.format(geo),'miles','minutes'])
	count = 0
	for file in filenames:
		with open(file, 'r') as f2:
			data = json.loads('[{}]'.format(f2.read().replace('\n',',')).replace('],]',']]'))
			for row in data:
				writer.writerow(row)
		count += 1
		if count % 100 == 0: print("On number {} of {}".format(count,len(filenames)))

print("")
print("Creating State Level Files")
print("")
print("Reading in data")
data = pd.read_csv('/home/ec2-user/output/{}_drive_times.csv'.format(geo))
print("Converting geographic identifiers")
print("  from")
data["from_{}".format(geo)] = [str(x).zfill(geo_length) for x in data["from_{}".format(geo)]]
print("  to")
data["to_{}".format(geo)] = [str(x).zfill(geo_length) for x in data["to_{}".format(geo)]]
print("Extracting States")
fips = ["01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53","54","55","56"]
for i in fips:
	print("  On state {}".format(i))
	data[([True if x[:2] == i else False for x in data["from_{}".format(geo)]]) | ([True if x[:2] == i else False for x in data["to_{}".format(geo)]])].to_csv('/home/ec2-user/output/{}_drive_times_{}'.format(geo,i), index = False)