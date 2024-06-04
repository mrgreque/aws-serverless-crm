from lambdas.process_data import process_data
from lambdas.read_data import read_data

def process_data_handler(event, context):
    return process_data(event, context)

def read_data_handler(event, context):
    return read_data(event, context)