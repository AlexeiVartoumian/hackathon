import json
import requests
import re
import random

def lambda_handler(event, context):
    
    category = event.get('category', 'fungi')  # default to fungi
    
    """
    way the website works is there is a a source/script/{category}Name js file .
    Insidew there are arrays that generate usernames . can directly request that .
    """
    js_url = f"https://www.fantasynamegenerators.com/scripts/{category}Names.js"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(js_url, headers=headers)
        response.raise_for_status()
        
        
        nm1_match = re.search(r'var nm1 = (\[.*?\]);', response.text, re.DOTALL)
        nm2_match = re.search(r'var nm2 = (\[.*?\]);', response.text, re.DOTALL)
        
        if nm1_match and nm2_match:
            
            nm1 = json.loads(nm1_match.group(1))
            nm2 = json.loads(nm2_match.group(1))
            
            
            names = []
            for i in range(10):
                name = f"{nm1[random.randint(0, len(nm1)-1)]} {nm2[random.randint(0, len(nm2)-1)]}"
                names.append(name)
            
            print(names)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'category': category,
                    'names': names,
                    'count': len(names)
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Could not find name arrays in JS file'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }