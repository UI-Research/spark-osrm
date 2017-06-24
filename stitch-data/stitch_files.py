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
	header = ['from_{}'.format(geo),'to_{}'.format(geo),'miles','minutes']
	writer.writerow(header)
	count = 0
	files = []
	writers = []
	fips = ["01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53","54","55","56"]
	reader_check = {}
	for i in range(len(fips)):
		files.append(open('/home/ec2-user/output/{}_drive_times_{}.csv'.format(geo,fips[i]), 'w'))
		reader_check[fips[i]] = i
		writers.append(csv.writer(files[i]))
		writers[i].writerow(header)
	for file in filenames:
		with open(file, 'r') as f2:
			data = json.loads('[{}]'.format(f2.read().replace('\n',',')).replace('],]',']]'))
			for row in data:
				writer.writerow(row)
				writers[reader_check[row[0][:2]]].writerow(row)
				writers[reader_check[row[1][:2]]].writerow(row)
		count += 1
		if count % 100 == 0: print("On file number {} of {}".format(count,len(filenames)))
	for i in range(len(files)):
		files[i].close()


