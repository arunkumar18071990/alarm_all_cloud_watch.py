import boto3
import pandas as pd

def fetch_all_instances():
    # Initialize the Boto3 client for EC2
    ec2_client = boto3.client('ec2')

    # Fetch all EC2 instances in the account
    response = ec2_client.describe_instances()

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)

    return instances

def fetch_instance_alarms(instance_id):
    # Initialize the Boto3 client for CloudWatch
    cloudwatch_client = boto3.client('cloudwatch')

    # Fetch all CloudWatch alarms
    alarms = cloudwatch_client.describe_alarms()

    # Filter alarms for the specific instance ID
    instance_alarms = []
    for alarm in alarms['MetricAlarms']:
        if instance_id in alarm['Dimensions'][0]['Value']:
            instance_alarms.append(alarm)

    return instance_alarms
"""
def remove_timezone_from_datetimes(alarms):
    for alarm in alarms:
        alarm['StateUpdatedTimestamp'] = alarm['StateUpdatedTimestamp'].replace(tzinfo=None)
        alarm['StateUpdatedTimestamp'] = alarm['StateUpdatedTimestamp'].replace(microsecond=0)

    return alarms

def export_to_excel(alarms, instance_id):
    alarms_no_timezone = remove_timezone_from_datetimes(alarms)
    df = pd.DataFrame(alarms_no_timezone)
    file_name = f"{instance_id}_alarms.xlsx"
    df.to_excel(file_name, index=False, engine="openpyxl")
    print(f"Alarm details exported to {file_name} successfully.")

def export_to_txt(alarms, instance_id):
    file_name = f"{instance_id}_alarms.txt"
    with open(file_name, 'w') as file:
        file.write(f"Alarms for instance {instance_id}:\n")
        for alarm in alarms:
            file.write(f"Alarm Name: {alarm['AlarmName']}\n")
            #file.write(f"Alarm Description: {alarm['AlarmDescription']}\n")
            file.write(f"Alarm State: {alarm['StateValue']}\n")
            file.write(f"Alarm Metric: {alarm['MetricName']}\n")
            file.write(f"Alarm Threshold: {alarm['Threshold']}\n")
            file.write(f"Alarm State Updated Timestamp: {alarm['StateUpdatedTimestamp']}\n")
            file.write("---\n")
    print(f"Alarm details exported to {file_name} successfully.")
"""
if __name__ == "__main__":
    all_instances = fetch_all_instances()

    for instance in all_instances:
        instance_id = instance['InstanceId']
        instance_alarms = fetch_instance_alarms(instance_id)

        if instance_alarms:
            print(f"Alarms for instance {instance_id}:")
            for alarm in instance_alarms:
                print(f"Alarm Name: {alarm['AlarmName']}")
                #print(f"Alarm Description: {alarm['AlarmDescription']}")
                print(f"Alarm State: {alarm['StateValue']}")
                print(f"Alarm Metric: {alarm['MetricName']}")
                print(f"Alarm Threshold: {alarm['Threshold']}")
                print(f"Alarm State Updated Timestamp: {alarm['StateUpdatedTimestamp']}")
                print(f"---")

            #export_to_excel(instance_alarms, instance_id)
            #export_to_txt(instance_alarms, instance_id)
        else:
            print(f"No alarms found for instance {instance_id}.")
