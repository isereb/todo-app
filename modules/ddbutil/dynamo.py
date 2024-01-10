import boto3
from modules.ddbutil.awsconfig import region

dynamodb = boto3.resource('dynamodb', region_name=region)
