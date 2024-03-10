import requests
import os

def get_json_files(repo_owner, repo_name, access_token, path=''):

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        json_files = []

        # Parse response JSON
        contents = response.json()

        # Loop through each item in the response
        for item in contents:
            if item['type'] == 'file':
                # Check if file has .json extension
                if item['name'] == 'metadata.json':
                    json_files.append(item['download_url'])
            elif item['type'] == 'dir':
                # Recursively get JSON files from subdirectories
                subdir_files = get_json_files(repo_owner, repo_name, access_token, f"{path}/{item['name']}")
                json_files.extend(subdir_files)
        return json_files
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
            response = requests.get(json_file)
            content = response.json()
            print(content)

    else:
        print("No JSON files found in the repository.")
