import requests
import os
import uuid
import mysql.connector
from models.service import Service

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

# DEV ENV
db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE_NAME
)

# Create a cursor object
cursor = db.cursor()

def get_metadata_json(repo_owner, repo_name, access_token, path=''):

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
                subdir_files = get_metadata_json(repo_owner, repo_name, access_token, f"{path}/{item['name']}")
                services.extend(subdir_files)
        return services
    else:
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")
        return None

def post_service(service):
    sql = "INSERT INTO services (id, name, owner) VALUES (%s, %s, %s)"
    val = (service.id, service.name, service.owner)
    cursor.execute(sql, val)
    print(f"Inserted {service.name} into the database")
    db.commit()

if __name__ == "__main__":

    REPO_OWNER = os.environ.get('REPO_OWNER')
    REPO_NAME = os.environ.get('REPO_NAME')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

    # Get JSON files from the repository
    services = get_metadata_json(REPO_OWNER, REPO_NAME, ACCESS_TOKEN)

    if services:
        print("JSON files found in the repository:")
        for service in services:
            post_service(service)
            # print(f"{service.id} \t {service.name} \t {service.owner}")
    else:
        print("No JSON files found in the repository.")

    db.close()
