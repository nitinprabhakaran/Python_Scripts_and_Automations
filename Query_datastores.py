import requests
from requests.auth import HTTPBasicAuth
import json
import base64

# Configuration
BITBUCKET_URL = "https://bitbucket.example.com"
USERNAME = "your_username"
PASSWORD = "your_password"

# Encode credentials for Basic Auth
credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode('utf-8')).decode('utf-8')

# Get all repositories
def get_repositories():
    url = f"{BITBUCKET_URL}/rest/api/1.0/repos"
    repos = []
    start = 0
    while True:
        response = requests.get(url, headers={"Authorization": f"Basic {credentials}"}, params={"start": start})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repositories: {response.text}")
        
        data = response.json()
        repos.extend(data['values'])
        if data['isLastPage']:
            break
        start = data['nextPageStart']
    return repos

# Get all files in a repository
def get_files(project_key, repo_slug):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/files"
    response = requests.get(url, headers={"Authorization": f"Basic {credentials}"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch files for {repo_slug}: {response.text}")
    
    return response.json()

# Check if file contains the string "mail:"
def file_contains_mail(project_key, repo_slug, file_path):
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/raw/{file_path}"
    response = requests.get(url, headers={"Authorization": f"Basic {credentials}"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file {file_path}: {response.text}")

    return "mail:" in response.text

def main():
    repos = get_repositories()
    print(f"Found {len(repos)} repositories")

    yaml_files_with_mail = []

    for repo in repos:
        project_key = repo['project']['key']
        repo_slug = repo['slug']
        print(f"Processing repository {repo_slug}")

        try:
            files = get_files(project_key, repo_slug)
        except Exception as e:
            print(f"Error fetching files for {repo_slug}: {e}")
            continue

        for file_path in files:
            if file_path.endswith(('.yaml', '.yml')):
                try:
                    if file_contains_mail(project_key, repo_slug, file_path):
                        yaml_files_with_mail.append((repo_slug, file_path))
                except Exception as e:
                    print(f"Error reading file {file_path} in {repo_slug}: {e}")
    
    # Print the result
    print("YAML files containing 'mail:'")
    for repo, file in yaml_files_with_mail:
        print(f"{repo}: {file}")

if __name__ == "__main__":
    main()