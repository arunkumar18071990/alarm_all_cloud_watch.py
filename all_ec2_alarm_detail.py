import boto3
import pandas as pd

def get_ec2_instances():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
            #print(instances)
    return instances


def get_instance_alarms(instance_id, cloudwatch_client):
    alarms = cloudwatch_client.describe_alarms(AlarmNamePrefix=f'CPUUtilization-{instance_id}')
    #print(alarms)
    return alarms['MetricAlarms']
def main():
    region = 'ap-south-1'  # Replace with your AWS region

    # Create a Boto3 CloudWatch client
    cloudwatch_client = boto3.client('cloudwatch', region_name=region)

    # Fetch all EC2 instances
    instances = get_ec2_instances()

    # Create a list to hold all alarm data
    all_alarms_data = []

    for instance in instances:
        instance_id = instance['InstanceId']
        alarms = get_instance_alarms(instance_id, cloudwatch_client)

        for alarm in alarms:
            all_alarms_data.append([
                instance_id,
                alarm['AlarmName'],
                alarm['AlarmDescription'],
                alarm['StateValue'],
                alarm['MetricName'],
                alarm['ComparisonOperator'],
                alarm['Threshold'],
                alarm['EvaluationPeriods'],
                alarm['Period']
            ])
            #print(alarm)

    # Create a Pandas DataFrame from the alarms data
    df = pd.DataFrame(all_alarms_data, columns=[
        'InstanceID', 'AlarmName', 'AlarmDescription', 'StateValue', 'MetricName',
        'ComparisonOperator', 'Threshold', 'EvaluationPeriods', 'Period'
    ])
    print(df)

    # Save the DataFrame to an Excel file
    filename = 'all_alarms.xlsx'
    df.to_excel(filename, index=False)

    print(f"Alarm details for all EC2 instances saved to {filename}.")

if __name__ == "__main__":
    main()
