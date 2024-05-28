import json
import boto3
import botocore

rds = boto3.client('rds')


def lambda_handler(event, context):
        # get all mariadb db instances
    rds_mariadb = rds.describe_db_instances(Filters=[
        {
            'Name': 'engine',
            'Values': ['mariadb']
            
        }])
    for db in rds_mariadb['DBInstances']:
        # start all rds instances
        try:
            state = db['DBInstanceStatus']
            if state == 'stopped':
                rds.start_db_instance(DBInstanceIdentifier=db['DBInstanceIdentifier'])
                print('Started instance: ' + db['DBInstanceIdentifier'])
            else:
                print('Instance ' + db['DBInstanceIdentifier'] + ' in state ' + state + ', skipping...')
        except botocore.exceptions.ClientError as err:
            print(err)
    return {
        'statusCode': 200,
        'body': json.dumps('Execution Completed!')
    }