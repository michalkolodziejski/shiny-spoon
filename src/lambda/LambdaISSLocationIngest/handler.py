import boto3
import urllib.request
import json
import datetime
import os

DYNAMODB_TABLE = region = os.environ['DYNAMODB_ISSLOCATION_TABLE']

print('Loading function')
dynamodb = boto3.resource('dynamodb')

def respond(err, res=None):
	return {
		'statusCode': '400' if err else '200',
		'body': err.message if err else json.dumps(res),
		'headers': {
			'Content-Type': 'application/json',
		},
	}


def lambda_handler(event, context):
	print("EVENT: ", event)

	url = "http://api.open-notify.org/iss-now.json"
	response = urllib.request.urlopen(url)
	result = json.loads(response.read())

	time = result["timestamp"]

	deviceid = "ISS"
	location = result["iss_position"]
	lat = location["latitude"]
	lon = location["longitude"]

	print(f"Latitude: {str(lat)}, Longitude: {str(lon)}")

	table = dynamodb.Table(DYNAMODB_TABLE)
	response = table.put_item(
		Item={
			'deviceid': deviceid,
			'time': time,
			'latitude': lat,
			'longitude': lon }
		)

	text = f'time={time} latitude={lat} longitude={lon}'
	message = '{"deviceid": "'+deviceid+'", "text": "'+text+'"}'

	return respond(None,json.loads(message))
