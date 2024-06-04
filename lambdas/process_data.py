import json
from client.s3 import S3
from helpers.transform_data import transform_data
from helpers.validate_body import validate_body
import logging

logger = logging.getLogger()
logger.setLevel("INFO")


print('test')
def process_data(event, context):
    erp_data = []
    invalids = []

    # read and validate the required fields from the event body
    try:
        event_body = json.loads(event['body'])
        logger.info(f'Event body: {event_body}')
        result = validate_body(event_body)

        if len(result['valids']) == 0:
            return {"statusCode": 400, "body": json.dumps(result['invalids'])}
        
        erp_data = result['valids']
        invalids = result['invalids']
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"message": "Error parsing event body"})}

    # save data to S3
    try:
        s3 = S3('crm-data-staging-erp-to-crm-bucket')

        # save ERP data to S3
        s3.upload(json.dumps(erp_data), 'erp_data.json')
        logger.info('ERP data saved to S3')

        # save transformed ERP data to S3 to be read by the next lambda
        s3.upload(json.dumps(transform_data(erp_data)), 'transformed_erp_data.json')
        logger.info('Transformed ERP data saved to S3')
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    
    body = {
        "message": "ERP data processed successfully",
        "imported_data": erp_data,
        "invalid_data": invalids
    }
    logger.info(body)

    return {"statusCode": 200, "body": json.dumps(body)}
