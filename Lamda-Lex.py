import boto3
import logging
import json


logger = logging.getLogger()
client = boto3.client('ses')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    name = str(event["currentIntent"]["slots"]["First_Name"].title())
    last = str(event["currentIntent"]["slots"]["Last_Name"].title())
    customer_email = str(event["currentIntent"]["slots"]["Email_Address"])
    item = dynamodb.put_item(TableName = "Table Name", Item = {"Email": {"S": customer_email},"Last Name": {"S": last}, "First_Name": {"S": name}})
    response = {
                "dialogAction":
                    {
                     "fulfillmentState":"Fulfilled",
                     "type":"Close","message":
                        {
                          "contentType":"PlainText",
                          "content": "Ok," + name + ",I have sent your information to our office and someone should be in contact with you shortly. I can assist you with any other questions you may have. Do you require any other assistance today? You can input things such as what are Basic Info, Game Status, of Game Info.",
                        },
                    }
                }
    email = client.send_email(
    Destination={
        'ToAddresses': [
            'Email Address',
        ],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': 'I spoke with {} {} today. {} can be reach via email at {}. Please contact him asap, as {} has requested contact.'.format(name, last, name, customer_email, name)
            },
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'Baymax spoke to {} {} today. This customer can be reached at {}'.format(name, last, customer_email),
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Baymax spoke to {} {}, please initiate contact'.format(name, last, customer_email),
        },
    },
    Source='From Email Address',
    SourceArn='',
    )
    logger.info("You were contacted by {}{} today".format(name, last))
    return response
