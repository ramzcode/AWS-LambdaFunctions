import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances(Filters=[{'Name': 'tag:AutoStop', 'Values': ['True']}])
    for reservation in instances.get("Reservations"):
        for instance in reservation.get("Instances"):
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            if state == 'stopped':
                ec2.start_instances(InstanceIds=[instance_id])
                print('Started instance: ' + instance_id)
            #elif state == 'started':
                #ec2.stop_instances(InstanceIds=[instance_id])
                #print('Stopped instance: ' + instance_id)
            else:
                print('Instance ' + instance_id + ' in state ' + state + ', skipping...')
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Instance check and start operation completed",
        }),
    }
