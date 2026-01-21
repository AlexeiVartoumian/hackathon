
import json
import boto3
import gspread
import random
import string
from google.oauth2.service_account import Credentials

SECRET_NAME = 'verysecret'
SPREADSHEET_ID = 'fantastic!'  
  
MAX_ROWS = 3  

def get_credentials():
    
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=SECRET_NAME)
    creds_dict = json.loads(response['SecretString'])
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return credentials

def find_next_empty_cell(worksheet):
 
   
    all_values = worksheet.get_all_values()
    

    max_col_to_check = max(10, len(all_values[0]) if all_values else 10)
    
    
    for col in range(1, max_col_to_check + 1):
        
        for row in range(1, MAX_ROWS + 1):
            try:
               
                cell_value = worksheet.cell(row, col).value
                
              
                if not cell_value or cell_value.strip() == '':
                    return (row, col)
            except:
               
                return (row, col)
    
    
    return (1, max_col_to_check + 1)

def generate_random_character():
  
    return random.choice(string.ascii_uppercase + string.digits)

def lambda_handler(event, context):
  
    
    try:
       
        creds = get_credentials()
        client = gspread.authorize(creds)
        
        
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = worksheet = spreadsheet.get_worksheet(0) #spreadsheet.worksheet(WORKSHEET_NAME)
        
        
        character = event.get('character') if event else None
        if not character:
            character = generate_random_character()
        
        
        row, col = find_next_empty_cell(worksheet)
        
        
        worksheet.update_cell(row, col, character)
        
      
        col_letter = chr(64 + col) if col <= 26 else f"Col{col}"
        
        print(f"Added '{character}' to cell {col_letter}{row}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Character added successfully',
                'character': character,
                'cell': f'{col_letter}{row}',
                'row': row,
                'column': col
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


if __name__ == '__main__':
    
    result = lambda_handler({}, None)
    print(json.dumps(result, indent=2))
    
    
    result = lambda_handler({'character': 'Z'}, None)
    print(json.dumps(result, indent=2))










# import json
# import logging


# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# def lambda_handler(event, context):

#     logging.info("forwarding rule exectued lambda")

#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }
