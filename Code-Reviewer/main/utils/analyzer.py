from groq import Groq
import uuid
from .github import fetch_pr_files, fetch_file_content
from .prompts import get_prompts


def analyze_code_with_llm(file_name, file_content):
    system_prompt, user_prompt = get_prompts(file_name, file_content)
    try:
        api_key = "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"
        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            temperature=0.7,
            top_p=0.9,
            response_format={"type": "json_object"},
        )
        return completion.choices[0].message.content
    
    except Exception as ex:
        print(ex)
        return None


def pr_analysis(repo_url, pr_number, github_token):
    analysis_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)

        analysis_result = []
        for file in pr_files:
            file_name = file['filename']
            file_content = fetch_file_content(repo_url, file_name, github_token)
            
            analysis_result = list(analyze_code_with_llm(file_name, file_content))
            analysis_result.append({"file_name": file_name, "result": analysis_result})

        return {"analysis_id": analysis_id, "result": analysis_result}
    
    except Exception as ex:
        print(ex)
        return {"analysis_id": analysis_id, "result": []}