from dotenv import load_dotenv
from groq import Groq
import os
import re

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client with API key from environment
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_with_llm(log_msg):
    """
    Classify a log message using an LLM via Groq API.
    Returns one of the following: 'Workflow Error', 'Deprecation Warning', or 'Unclassified'.
    """
    prompt = f'''Classify the log message into one of these categories: 
(1) Workflow Error, (2) Deprecation Warning.
If you can't figure out a category, use "Unclassified".
Put the category inside <category> </category> tags.
Log message: {log_msg}'''

    try:
        chat_completion = groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="deepseek-llm-r1-70b",  # fixed model name
            temperature=0.5
        )
        content = chat_completion.choices[0].message.content
        match = re.search(r'<category>(.*?)</category>', content, re.DOTALL)
        return match.group(1).strip() if match else "Unclassified"

    except Exception as e:
        print(f"Error during LLM classification: {e}")
        return "Unclassified"

if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))
