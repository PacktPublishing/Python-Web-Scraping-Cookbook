from urllib.request import urlopen
from bs4 import BeautifulSoup

import boto3
import botocore

# create sqs client
sqs = boto3.client('sqs', "us-west-2")

# create / open the SQS queue
queue = sqs.create_queue(QueueName="PlanetMoreInfo")
print (queue)

# read and parse the planets HTML
html = urlopen("http://127.0.0.1:8080/pages/planets.min.html")
bsobj = BeautifulSoup(html, "lxml")

planets = []
planet_rows = bsobj.html.body.div.table.findAll("tr", {"class": "planet"})

for i in planet_rows:
	tds = i.findAll("td")
	
	# get the URL
	more_info_url = tds[5].findAll("a")[0]["href"].strip()
	
	# send the URL to the queue
	sqs.send_message(QueueUrl=queue["QueueUrl"],
					 MessageBody=more_info_url)
	print("Sent %s to %s" % (more_info_url, queue["QueueUrl"]))