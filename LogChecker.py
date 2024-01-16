import os
import requests

def extract_user_ids(input_file, output_file):
    unique_user_ids = set()

    # Get the script's directory and construct paths
    script_directory = os.path.dirname(__file__)
    input_path = os.path.join(script_directory, input_file)
    output_path = os.path.join(script_directory, output_file)

    print("Absolute path to input file:", os.path.abspath(input_path))

    # Function to get user information from the API
    def get_user_info(user_id):
        api_url = f'https://users.roblox.com/v1/users/{user_id}'
        response = requests.get(api_url)
        if response.status_code == 200:
            user_info = response.json()
            return user_info.get("name", ""), user_info.get("displayName", ""), user_info.get("id", "")
        else:
            return "", "", ""

    with open(input_path, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
            # Assuming the format '"userId" : {number}'
            if '"userId" :' in line:
                # Extract the number after "userId"
                user_id = line.split('"userId" :')[-1].strip().rstrip(',')
                # Check if user ID has not been processed before
                if user_id not in unique_user_ids:
                    unique_user_ids.add(user_id)
                    
                    # Get user information from the API
                    name, display_name, user_id_api = get_user_info(user_id)
                    
                    # Print user information
                    print(f"Checking user: {name}")
                    
                    # Write user information to the output file
                    with open(output_path, 'a') as output:
                        output.write(f"Name: {name}, DisplayName: {display_name}, ID: {user_id_api}\n")

    print("Finished checking users.")
    # Keep the program open
    input("Press Enter to exit...")

# Use 'input.txt' as the input file and 'output.txt' as the output file
extract_user_ids('input.txt', 'output.txt')
