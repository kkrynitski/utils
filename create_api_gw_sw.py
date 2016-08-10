from pprint import pprint
import requests
import json
import boto3
import os


url = 'http://127.0.0.1:5000/todos/api'
if requests.get(url).status_code == 200:
    print "Status code: 200"
else:
    print "Wrong response from api"
    exit()


with open('api_swagger.json', 'w' ) as file_:
   file_.write(json.dumps(requests.get(url).json(), indent=4, sort_keys=True, separators=(',', ':')))
file_.close()

client = boto3.client('apigateway')

body_file = os.path.abspath('api_swagger.json')

if os.path.exists(body_file):
    with open(body_file, 'r') as f:
        import_rest_api = client.import_rest_api(
            failOnWarnings=True,
            body=f
        )
    with open('api_gw_id.log', 'w') as log_file:
        log_file.write(import_rest_api["id"])
    log_file.close()
else:
    print "File with swagger specs does not exist"
    exit()
pprint(import_rest_api)
print ""
print ""
print "Api GW ID: ",import_rest_api['id']
