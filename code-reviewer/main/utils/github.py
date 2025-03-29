from urllib.parse import urlparse
import requests
import base64
import time


def get_owner_and_repo(url):
    passed_url = urlparse(url)
    path_parts = passed_url.path.strip("/").split("/")
    if len(path_parts) >= 2:
        owner, repo = path_parts[0], path_parts[1]
        return owner, repo
    return None, None


def fetch_pr_files(repo_url, pr_number, github_token=None, max_retries=3):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            pr_files = response.json()

            if not isinstance(pr_files, list): 
                print(f"Unexpected API response: {pr_files}")
                return []
            
            return pr_files
        
        except requests.exceptions.RequestException as ex:
            print(f"Attempt {attempt+1}: Error fetching PR files: {ex}")
            time.sleep(5)  
                
    print("Max retries reached. Skipping request.")
    return None


def fetch_file_content(repo_url, pr_branch, file_path, github_token=None, max_retries=3):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={pr_branch}"

    headers = {"Authorization": f"token {github_token}"} if github_token else {}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                print(f"File not found: {file_path} in branch {pr_branch}")
                return None
            try:
                response.raise_for_status()
                content = response.json() 
            except requests.exceptions.JSONDecodeError:
                print(f"Failed to decode JSON response for {file_path}")
                return None

            # Handling large files by using the "download_url"
            if "download_url" in content and content["download_url"]:
                for file_attempt in range(max_retries):
                    try:
                        file_response = requests.get(content["download_url"], timeout=10)
                        file_response.raise_for_status()
                        return file_response.text  
                    except requests.exceptions.RequestException as e:
                        print(f"Attempt {file_attempt+1}: Error fetching large file {file_path}: {e}")
                        time.sleep(2 ** file_attempt)  

            return base64.b64decode(content["content"]).decode()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}: Error fetching {file_path}: {e}")
            time.sleep(2 ** attempt) 

    print(f"Max retries reached. Could not fetch file: {file_path}")
    return None
