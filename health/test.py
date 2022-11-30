import requests
try:
    requests.get('http://acit3855-kafka-lab6.eastus.cloudapp.azure.com:8110/health',timeout=3)
except Exception as e:
    print(e)
