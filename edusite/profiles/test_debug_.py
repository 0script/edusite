import subprocess

import os
import json

def create_json_file(destination, subject, message):
    # Create the subdirectory if it does not exist
    subdirectory = 'send_gmail'
    if not os.path.exists(subdirectory):
        raise Exception('dir do not exist ')
    
    # Prepare the data to be written to the JSON file
    data = {
        'destination': destination,
        'subject': subject,
        'message': message
    }
    
    # Define the file path
    file_path = os.path.join(subdirectory, 'email.json')
    
    # Write the data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"JSON file created at {file_path}")

# Example usage
create_json_file('nkogheobame.marcel@gmail.com', 'Greetings', 'Hello, how are you?')
subprocess.call('cd send_gmail/; python3 send_email.py', shell=True)

print('ok ok')