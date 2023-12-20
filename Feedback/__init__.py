import logging

import azure.functions as func


def main(req: func.HttpRequest, outdoc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Feedback Endpoint called.')



    try: 
            req_body = req.get_json() 
    except ValueError: 
            return func.HttpResponse( 
                "Please pass a JSON in the request body", 
                status_code=400 
            ) 
    conversation_id = req_body.get('conversationId')
    feedback = req_body.get('feedback')
    response_id = req_body.get('responseId')
    if len(req_body) > 3:
        return func.HttpResponse(
             "Please pass only conversationID, feedback and responseId in the request body",
             status_code=400
        )
    if not conversation_id:
        return func.HttpResponse(
             "Please pass a conversationId in the request body",
             status_code=400
        )
    if not feedback:
        return func.HttpResponse(
             "Please pass a feedback in the request body",
             status_code=400
        )
    #feedback can only be [-1,0,1]
    if feedback not in [-1,0,1]:
        return func.HttpResponse(
             "Please pass a valid feedback in the request body",
             status_code=400
        )
    if not response_id:
        return func.HttpResponse(
             "Please pass a responseId in the request body",
             status_code=400
        )
    try:
        outdoc.set(func.Document.from_json(req.get_body()))
    except Exception as e:
        return func.HttpResponse(
             "Error: {}".format(e),
             status_code=400
        )
    return func.HttpResponse(
             "This HTTP triggered function executed successfully. Your Respose was recorded.",
             status_code=200
        )
    