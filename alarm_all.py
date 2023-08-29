import boto3
import pandas as pd

# AWS credentials and region
#aws_access_key_id = 'YOUR_AWS_ACCESS_KEY'
#aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
#region_name = 'YOUR_AWS_REGION_NAME'

# Initialize AWS clients
region = 'ap-south-1' 
ec2_client = boto3.client('ec2')
cloudwatch_client = boto3.client('cloudwatch',region_name = region)

# Function to get alarm details for an instance
def get_instance_alarms(instance_id):
    alarms = cloudwatch_client.describe_alarms(AlarmNamePrefix=f'{instance_id}-')
    return alarms['MetricAlarms']

# Function to get all instances in the account
def get_all_instances():
    instances = ec2_client.describe_instances()
    return [instance for reservation in instances['Reservations'] for instance in reservation['Instances']]

# Get all instances
instances = get_all_instances()

# List to store alarm details
alarm_details = []

# Fetch alarm details for each instance
for instance in instances:
    instance_id = instance['InstanceId']
    instance_name = [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']
    instance_name = instance_name[0] if instance_name else '-'
    
    alarms = get_instance_alarms(instance_id)
    
    for alarm in alarms:
        alarm_details.append({
            'Instance ID': instance_id,
            'Instance Name': instance_name,
            'Alarm Name': alarm['AlarmName'],
            'Metric Name': alarm['MetricName'],
            'Alarm Description': alarm['AlarmDescription'],
            'Alarm State': alarm['StateValue'],
            'Alarm Actions': ', '.join(alarm.get('AlarmActions', [])),
        })

# Create a DataFrame from the alarm details
df = pd.DataFrame(alarm_details)

# Save the DataFrame to an Excel file
df.to_excel('aws_alarm_details.xlsx', index=False)
