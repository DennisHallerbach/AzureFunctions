import logging

import azure.functions as func
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import requests
import json
import time



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    subscription_id = "52c47fda-2dd0-429a-a46c-62173b26a70f"
    resource_group = "Ai-PoC"
    workspace = "gep-aipoc-azureml"
    endpoint_name = "gep-aipoc-endpoint"
    ml_client = MLClient(
        DefaultAzureCredential(), subscription_id, resource_group, workspace
    )
    api_key = ml_client.online_endpoints.get_keys(name=endpoint_name).access_token

    #body = str.encode(req.get_body())
    body = req.get_body()
    logging.info(body)
    url = 'https://gep-aipoc-endpoint.swedencentral.inference.ml.azure.com/score'
    #url2 = 'https://gep-aipoc-endpoint.swedencentral.inference.ml.azure.com/swagger.json'
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    #req2 = urllib.request.Request(url2, headers=headers)
    #req = urllib.request.Request(url, body, headers)
    r =  requests.get(url, stream=True, headers=headers)
    headers2 = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }

    response = func.HttpResponse(headers=headers)

    # Send the response to the client in real-time using SSE
    response.streaming = True
    # Send the headers to the client
    response = func.HttpResponse(headers=headers)
    response.write('event: message\n')
    response.write('data: {}\n\n'.format(json.dumps({'response': 'Processing...'})))

    
    logging.info(r)
    for line in r.iter_lines():

        # filter out keep-alive new lines
        if line:
            logging.info(line)
            response.write('event: message\n')
            response.write('data: {}\n\n'.format(json.dumps({'response': str(line).strip()})))
            time.sleep(1)

    return response

    