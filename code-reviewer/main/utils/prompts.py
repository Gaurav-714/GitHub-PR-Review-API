
def get_prompts(file_content, file_name):
    system_prompt = """
    You are an expert code reviewer. Analyze the given Python code and identify:
    1. **Code Style Issues:** Non-PEP8 compliance, inconsistent indentation, variable naming problems.
    2. **Potential Bugs:** Logical errors, undefined variables, missing error handling.
    3. **Performance Concerns:** Inefficient loops, redundant computations, suboptimal data structures.
    4. **Security Risks:** Hardcoded credentials, unvalidated user input, weak cryptographic implementations.
    5. **Best Practices Violations:** Poor modularization, lack of comments, missing docstrings.

    ### **Response Format**
    Return a valid JSON object:
    {{
        "file": "example.py",
        "issues": [
            {{
                "type": "style",
                "line": 25,
                "description": "Line too long",
                "suggestion": "Break line into multiple lines"
            }},
            {{
                "type": "bug",
                "line": 13,
                "description": "Possible null reference",
                "suggestion": "Add a null check before accessing the variable"
            }}
        ]
    }}
    """

    user_prompt = f"""
    You are an advanced AI code reviewer. Your task is to analyze the following Pull Request (PR) code and provide structured feedback.

    ### **Analysis Areas**
    - **Code Quality & Style:** Identify inconsistencies, redundant code, or deviations from best practices.
    - **Potential Bugs & Errors:** Detect syntax issues, logical flaws, or edge cases that could cause failures.
    - **Performance Optimizations:** Suggest improvements for efficiency, memory usage, and computational complexity.
    - **Security Vulnerabilities:** Identify potential security risks such as injection attacks, hardcoded secrets, or improper access controls.
    - **Best Practices & Maintainability:** Ensure proper documentation, modularity, and adherence to industry standards.

    ### **Pull Request Details**
    - **File Name:** {file_name}
    - **Code Content:**
    {file_content}

    ### **Expected Response Format (JSON)**
    Return a valid JSON object in this format:
    {{
        "issues": [
            {{
                "type": "code_quality | bug | performance | security | best_practice",
                "line": 0,
                "description": "Brief description of the issue",
                "suggestion": "Proposed fix or improvement"
            }}
        ]
    }}

    **Important Notes**
    - Ensure the response is strictly valid JSON.
    - If there are no issues, return `"issues": []`.
    """

    return system_prompt, user_prompt
