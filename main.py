import requests

def get_file_contents(repo_url, branch, filename):
  """Fetches the contents of a file from a GitHub repository.

  Args:
      repo_url: The URL of the GitHub repository (e.g., "https://github.com/user/repo").
      branch: The branch to search (defaults to "master").
      filename: The name of the file to retrieve.

  Returns:
      The contents of the file as a string, or None if the file is not found.
  """
  url = f"{repo_url}/contents/{branch}/{filename}"
  headers = {"Authorization": f"token YOUR_GITHUB_ACCESS_TOKEN"}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    data = response.json()
    return data["content"].encode("utf-8").decode("base64")  # Decode base64 encoded content
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None

if __name__ == "__main__":
  # Replace with your actual values
  repo_url = "https://github.com/user/repo"
  branch = "master"  # Optional, defaults to "master"
  filename = "myfile.txt"

  # Generate a personal access token from your GitHub account settings: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
  # Replace 'YOUR_GITHUB_ACCESS_TOKEN' with the generated token
  access_token = "YOUR_GITHUB_ACCESS_TOKEN"

  contents = get_file_contents(repo_url, branch, filename)

  if contents:
    print(contents)
  else:
    print(f"File '{filename}' not found in repository.")
