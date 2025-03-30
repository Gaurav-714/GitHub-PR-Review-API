import os
import groq
import json
import uuid
import time
import requests
from .prompts import get_prompts
from .github import fetch_pr_files, fetch_file_content


def analyze_code_with_llm(file_name, file_content):
    system_prompt, user_prompt = get_prompts(file_name, file_content)

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Set the GROQ_API_KEY environment variable.")

    client = groq.Groq(api_key=api_key)
    
    max_attempts = 3
    wait_time = 10  

    for attempt in range(max_attempts): 
        try:  
            #model="llama-3.3-70b-versatile", 
            #model="llama-3.2-3b-preview", 
            completion = client.chat.completions.create( 
                model="llama-3.1-8b-instant",
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                temperature=0.7,
                top_p=0.9,
                response_format={"type": "json_object"},
            )
            response_content = completion.choices[0].message.content.strip()

            try:
                json_response = json.loads(response_content)  
            except json.JSONDecodeError:
                json_response = {"response": response_content}  

            return json_response 
        
        except requests.exceptions.RequestException as ex: 
            print(f"Network error: {ex}")
            wait_time *= 2 
            time.sleep(wait_time)

        except Exception as ex:
            print(f"Error while calling Groq API: {ex}")

    print("Max retries reached. Skipping this request.")        
    return None  


def pr_analysis(repo_url, pr_branch, pr_number, github_token, max_retries=3):
    analysis_id = str(uuid.uuid4())
    analysis_result = []
    errors = []
    
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token, max_retries)
        if isinstance(pr_files, dict) and "error" in pr_files:
            return {"analysis_id": analysis_id, "status": "FAILED", "error": pr_files["error"]}
        if not isinstance(pr_files, list):
            return {"analysis_id": analysis_id, "status": "FAILED", "error": "Unexpected API response format."}

        for file in pr_files:
            file_name = file.get("filename") # file["filename"]
            if not file_name:
                continue

            file_path_parts = file_name.split("/") 
            if any(part == "__pycache__" for part in file_path_parts) or file_name.endswith((".pyc", ".sqlite3")):
                continue

            file_content = fetch_file_content(repo_url, pr_branch, file_name, github_token, max_retries)
            if isinstance(file_content, dict) and "error" in file_content:
                errors.append(f"Skipping {file_name}: {file_content['error']}")
                continue
            if not isinstance(file_content, str):
                errors.append(f"Skipping {file_name}: Unexpected response format.")
                continue

            file_analysis = analyze_code_with_llm(file_name, file_content)
            if file_analysis:
                analysis_result.append({"file_name": file_name, "analysis": file_analysis})
            
        if not analysis_result:
            return {
                "analysis_id": analysis_id,
                "status": "FAILED",
                "error": "All files failed to process.",
                "details": errors
            }

        return {"analysis_id": analysis_id, "status": "SUCCESS", "result": analysis_result}
    
    except Exception as ex:
        print(f"Error in PR analysis: {ex}")
        return {
            "analysis_id": analysis_id,
            "status": "FAILED",
            "result": [],
            "details": errors
        }
    