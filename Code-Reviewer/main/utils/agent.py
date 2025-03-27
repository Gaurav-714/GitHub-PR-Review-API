from groq import Groq
from .prompts import get_prompts


def analyze_code_with_llm(file_content, file_name):
    system_prompt, user_prompt = get_prompts(file_content, file_name)

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

