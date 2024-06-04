# validate_body function is used to validate the event body received by the process_data lambda. 
# it checks if the expected keys are present in the event body and returns a dictionary with the valid and invalid items. 
# if an item is invalid, it adds an errors key to the item with the error message.
def validate_body(event_body):
    expected_keys = ['id', 'valor', 'data', 'frete', 'desconto', 'status']

    validation_result = {
        'valids': [],
        'invalids': []
    }
    for item in event_body:
        for key in expected_keys:
            if key not in item:
                item['errors'] = f"Key {key} not found in event body" if 'errors' not in item else item['errors'] + f", Key {key} not found in event body"

        if 'errors' in item:
            validation_result['invalids'].append(item)
        else:
            validation_result['valids'].append(item)
        
    return validation_result