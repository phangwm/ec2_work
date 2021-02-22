#!/usr/bin/python3

import json
import boto3

def ec2_work(action):
    region = "ap-southeast-1"
    client = boto3.client('ec2', region)
    responce = client.describe_instances(Filters=[{'Name': 'tag:AutoShutdown', "Values": ['Yes']},{'Name':'instance-state-name',"Values": ['running']}])

    target_instans_ids = []
    target_instans_name = []
    for reservation in responce['Reservations']:
      for instance in reservation['Instances']:
        tag_name = ''
        for tag in instance['Tags']:
          if tag['Key'] == 'Name':
            tag_name = tag['Value']
            break

        target_instans_ids.append(instance['InstanceId'])
        target_instans_name.append(tag_name)

   # print(target_instans_ids)
   # print(target_instans_name)

    if not target_instans_ids:
      print('There are no instances subject to automatic start / stop.')
    else:
      if action == 'start':
        client.start_instances(InstanceIds=target_instans_ids)
        print('started instances.')
      elif action == 'stop':
        #client.stop_instances(InstanceIds=target_instans_ids)
        print('stopped instances.')
      else:
        print('Invalid action.')

    # Email
    Instance_list=''
    for x in target_instans_name:
      Instance_list = Instance_list + "<br/>" + x

    BODY_HTML = "<html> <head></head> <body> <h1>WX-Dev: Daily Auto Shutdown EC2</h1>  <p>The following instances are auto shutdown<br/> " + Instance_list + "</p> </body> </html>"
    SENDER = "wmphang@gmail.com"
    RECIPIENT = "wmphang@gmail.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "WX-Dev: Daily Auto Shutdown EC2"
    CHARSET = "UTF-8"
    client2 = boto3.client('ses',region_name=AWS_REGION)

    response = client2.send_email(
      Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                }
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
     Source=SENDER,
    )
    return 


ec2_work("stop");
