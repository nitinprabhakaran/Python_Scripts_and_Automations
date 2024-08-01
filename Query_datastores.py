import requests
from requests.auth import HTTPBasicAuth

# Function to get the project name from Bitbucket Server API
def get_project_name(base_url, project_key, username, password):
    url = f"{base_url}/rest/api/1.0/projects/{project_key}"

    # Make the API request
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    # Check if the request was successful
    if response.status_code == 200:
        project_data = response.json()
        return project_data.get("name", "Project name not found")
    else:
        return f"Failed to retrieve project. Status code: {response.status_code}"

# Main script
if __name__ == "__main__":
    # Input the required details
    base_url = input("Enter the Bitbucket Server base URL (e.g., https://bitbucket.example.com): ")
    project_key = input("Enter the project key: ")
    username = input("Enter your Bitbucket username: ")
    password = input("Enter your Bitbucket password: ")

    # Get the project name
    project_name = get_project_name(base_url, project_key, username, password)
    print(f"Project Name: {project_name}")