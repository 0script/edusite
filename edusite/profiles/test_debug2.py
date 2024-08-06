from datetime import datetime, timedelta
import uuid

def create_unique_identifier(current_date_str, name):
    # Convert the input string to a datetime object
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d %H:%M:%S')
    
    # Add 24 hours to the current date
    updated_date = current_date + timedelta(hours=24)
    
    # Create a unique identifier
    unique_id = f"{updated_date.strftime('%Y%m%d%H%M%S')}_{name}_{uuid.uuid4()}"
    
    return unique_id

import uuid

def parse_unique_identifier(unique_id):
    # Split the unique_id into its components
    try:
        date_str, name, _ = unique_id.split('_')
        
        # Convert the date string back to a datetime object
        date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
        
        return date, name
    except ValueError:
        print("Invalid unique identifier format.")
        return None

# Example usage


# Example usage
formatted_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
name="eleviator"
unique_id = create_unique_identifier(formatted_date_time, name)
print(unique_id)

print('reverso')
parsed_date, parsed_name = parse_unique_identifier(unique_id)
print(f"Date: {parsed_date}")
print(f"Name: {parsed_name}")
