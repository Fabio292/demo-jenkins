import requests
import json
import os
import sys

#environmental variables
imagetag=os.environ.get("IMAGETAG")
buildid=os.environ.get("BUILD_ID")
high_t=os.environ.get("HIGH")
medium_t=os.environ.get("MEDIUM")
low_t=os.environ.get("LOW")
negligible_t=os.environ.get("NEGLIGIBLE")
unknown_t=os.environ.get("UNKNOWN")
user=os.environ.get("USER")
password=os.environ.get("PASSWORD")

def requestToken():
    url = "a53bcb22c40af11eaacb70ae5ec6da6f-1483260547.us-east-1.elb.amazonaws.com/api/sessions"
    headers = {'Content-Type': 'application/json'}
    data = {'user': {'userID': user, 'password': password}}

    try:
        response = requests.request("POST", url, json=data, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    return response.json()['token']

def requestScan():
    url = "a53bcb22c40af11eaacb70ae5ec6da6f-1483260547.us-east-1.elb.amazonaws.com/api/scans"
    data = {"source": {
        "type": "docker",
        "registry": "https://089058466443.dkr.ecr.eu-north-1.amazonaws.com",
        "repository": "fabio-demo",
        "tag": imagetag+'-'+buildid,
        "credentials": {"aws": {"region": "<region>"}}},
       
        
    try:
        response = requests.request("POST", url, json=data, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    return response.json()['id']

def requestReport():
    high, medium, low, negligible, unknown = 0, 0, 0, 0, 0
    status='pending'

    url = "a53bcb22c40af11eaacb70ae5ec6da6f-1483260547.us-east-1.elb.amazonaws.com/api/scans/"
    headers = {'Authorization': 'Bearer'+requestToken()}
    querystring = {"id": requestScan(),"expand":"none"}

    while status != "completed-with-findings":
        try:
            response=requests.request("GET", url, headers=headers,params=querystring,verify=False)
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit(1)

        status = response.json()['scans'][0]['status']
        
        if (status == "completed-no-findings"):
            break

        if status == 'failed':
            print("Scan failed!")
            sys.exit(1)

    data = response.json()

    if(status == "completed-with-findings" ):
        findings = data['scans'][0]['findings']
        vulnerabilities = findings['vulnerabilities']

        dataVuln = "Vulnerabilities found: \n"
        dataMalw = ""

        for value in vulnerabilities['total']:
            if value == 'high':
                high = vulnerabilities['total']['high']
                dataVuln = dataVuln+"High: "+str(high)+"\n"
            if value == 'medium':
                medium = vulnerabilities['total']['medium']
                dataVuln = dataVuln+"Medium: "+str(medium)+"\n"
            if value == 'low':
                low = vulnerabilities['total']['low']
                dataVuln = dataVuln+"Low: "+str(low)+"\n"
            if value == 'negligible':
                negligible = vulnerabilities['total']['negligible']
                dataVuln = dataVuln+"Negligible: "+str(negligible)+"\n"
            if value == 'unknown':
                unknown = vulnerabilities['total']['unknown']
                dataVuln = dataVuln+"Unknown: "+str(unknown)+"\n"
        
        if dataVuln == "Vulnerabilities found: \n": dataVuln=""

        for value in findings:
            if value == 'malware':
                malware = findings['malware']
                dataMalw = "Malware found: "+str(malware)

        message = dataVuln+dataMalw

    if (high <= int(high_t)) and (medium <= int(medium_t)) and (low <= int(low_t)) and (negligible <= int(negligible_t)) and (unknown <= int(unknown_t) and (malware < 1)):
        sys.stdout.write('1')
        message = "Image is clean and ready to be deployed!"

    sendToSlack(message)

requestReport()
