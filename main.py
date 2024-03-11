import requests
import os
import uuid
from models.service import Service

def get_json_files(repo_owner, repo_name, access_token, path=''):

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {'Authorization': f'token {access_token}'}

    services = []

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # Parse response JSON
        contents = response.json()
        # Loop through each item in the response
        for item in contents:
            if item['type'] == 'file':
                # Check if file has .json extension
                if item['name'] == 'metadata.json':
                    # Make request and parse the response
                    response = requests.get(item['download_url'])
                    content = response.json()
                    # Map the response to a Model
                    new_service = Service(
                        id=str(uuid.uuid4()),
                        name=content['name'],
                        owner=content['owner']
                    )
                    # append the service to an array
                    services.append(new_service)
            elif item['type'] == 'dir':
                # Recursively get JSON files from subdirectories
                subdir_files = get_json_files(repo_owner, repo_name, access_token, f"{path}/{item['name']}")
                services.extend(subdir_files)
        return services
    else:
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")
        return None

if __name__ == "__main__":

    REPO_OWNER = os.environ.get('REPO_OWNER')
    REPO_NAME = os.environ.get('REPO_NAME')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

    # Get JSON files from the repository
    json_files = get_json_files(REPO_OWNER, REPO_NAME, ACCESS_TOKEN)

    if json_files:
        print("JSON files found in the repository:")
        for json_file in json_files:
            print(f"{json_file.id} \t {json_file.name} \t {json_file.owner}")
    else:
        print("No JSON files found in the repository.")
