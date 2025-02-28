import birthday_emailer

def lambda_handler(event, context):
    birthday_emailer.main()
    return {
        'statusCode': 200,
        'body': 'Birthday check completed'
    } 