
import json
import sys
import boto3



def upload_creds(file_path):

    with open(file_path , "r") as f :
        credentials = json.load(f)
    

    client = boto3.client("secretsmanager")


    secret_name = "somethingverysecretive"


    try:

        response = client.create_secret(
            Name = secret_name,
            Description='Google sheets api sercie account credentials',
            SecretString= json.dumps(credentials) 
        )
    
    except client.exceptions.ResourceExistsException:

        response = client.update_secret(
            SecretId=secret_name,
            SecretString=json.dumps(credentials)
        )
        print(f"  ARN: {response['ARN']}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
       
        sys.exit(1)
json_file=sys.argv[1]
upload_creds(json_file)