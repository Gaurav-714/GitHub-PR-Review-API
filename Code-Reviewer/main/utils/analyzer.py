from groq import Groq
import os
import uuid
import openai
import time
import json
from .github import fetch_pr_files, fetch_file_content
from .prompts import get_prompts


def analyze_code_with_llm(file_name, file_content):
    system_prompt, user_prompt = get_prompts(file_name, file_content)
    api_key = "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"
    #api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Set the GROQ_API_KEY environment variable.")

    client = Groq(api_key=api_key)
    for attempt in range(3):  # Retry up to 3 times
        try:   
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                temperature=0.7,
                top_p=0.9,
                #response_format={"type": "json_object"},
            )
            response_dict = json.loads(completion.model_dump_json())  
            #print(f"LLM Response for {file_name}: {response_dict}")
            return response_dict
            #return completion.choices[0].message.content
        
        except openai.error.RateLimitError:
                wait_time = (attempt + 1) * 10  # Increase wait time exponentially
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        except Exception as ex:
            print(f"Error while calling Groq API: {ex}")
        
    return None 


def pr_analysis(repo_url, pr_number, github_token):
    analysis_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)
        analysis_result = []

        for file in pr_files:
            file_name = file['filename']
            file_content = fetch_file_content(repo_url, file_name, github_token)
            
            file_analysis = analyze_code_with_llm(file_name, file_content)
            if file_analysis is not None:
                analysis_result.append({"file_name": file_name, "result": file_analysis})

        print(f"Final Analysis Result: {json.dumps(analysis_result, indent=2)}")
        return {"analysis_id": analysis_id, "status": "SUCCESS", "result": analysis_result}
    
    except Exception as ex:
        print(ex)
        return {"analysis_id": analysis_id, "status": "FAILED", "result": []}
    