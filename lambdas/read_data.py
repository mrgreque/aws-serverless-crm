import json
from client.s3 import S3
import urllib3
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def read_data(event, context):
    # get the bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    logger.info(f'Bucket: {bucket_name}, Object: {object_key}')

    # read transformed data from S3
    s3 = S3(bucket_name)
    transformed_data = s3.read_file(object_key)
    logger.info(f'Data: {transformed_data}')

    # send data to CRM
    crm_url = 'http://httpbin.org/post'
    headers = {'Content-Type': 'application/json'}
    http = urllib3.PoolManager()
    response = http.request(
        'POST',
        crm_url,
        body=transformed_data,
        headers=headers
    )
    logger.info(f'Response: {response.status}')

    if response.status != 200:
        logger.error('Failed to send data to CRM')
        return {
            'statusCode': response.status,
            'body': json.dumps({'message': 'Failed to send data to CRM'})
        }
    
    logger.info('Data sent to CRM successfully')
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data sent to CRM successfully'})
    }