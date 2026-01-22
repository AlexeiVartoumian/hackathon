import json
import requests
import re

def hello(event, context):
    url = "https://www.fantasynamegenerators.com/fungi-names.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # Make the request
        print("making requesr")
        response = requests.get(url , headers = headers)
        response.raise_for_status()
        print("=" * 50)
        print("RESPONSE CONTENT:")
        print(response.text)
        print("=" * 50)
        # Extract the content between <div id="result"> and </div>
        match = re.search(r'<div id="result">(.*?)</div>', response.text, re.DOTALL)
        
        if match:
            
            content = match.group(1)
            names = [name.strip() for name in content.split('<br>') if name.strip()]
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'names': names,
                    'count': len(names)
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Could not find result div'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    

hello("hi" ,"hi")