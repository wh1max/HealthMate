import os
import openai
import json

# Read configuration from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "gpt-oss-20b:free")
SITE_URL = os.getenv("SITE_URL", "http://localhost:5000") # Your website URL

# Initialize the OpenAI client with the correct base URL for OpenRouter
client = openai.OpenAI(
    api_key=API_KEY,
    base_url=API_BASE,
    default_headers={
        "HTTP-Referer": SITE_URL,
        "X-Title": "HealthMate AI", # Optional, but recommended
    },
)

def analyze_symptoms(symptoms_text):
    """
    Analyzes user's symptoms using an AI model to generate clarifying questions.
    """
    try:
        prompt = f"""
        A user is reporting the following symptoms: "{symptoms_text}".
        Based on these symptoms, generate exactly 5 simple and clear yes/no questions to help clarify the situation.
        Return the questions as a JSON-formatted list of strings.
        For example: ["Do you have a fever?", "Are you experiencing body aches?"]
        """
        
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant that asks clarifying questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        
        questions_str = response.choices[0].message.content
        questions = json.loads(questions_str)
        
        # Basic validation to ensure we have a list of 5 strings
        if isinstance(questions, list) and len(questions) == 5 and all(isinstance(q, str) for q in questions):
            return {
                "symptoms": [s.strip() for s in symptoms_text.lower().split('and')],
                "questions": questions
            }
        else:
            raise ValueError("AI did not return the expected format.")

    except Exception as e:
        print(f"Error calling AI or parsing response: {e}")
        # Fallback to mock questions if AI fails
        return {
            "symptoms": [s.strip() for s in symptoms_text.lower().split('and')],
            "questions": [
                "Have you had a fever recently?",
                "Are you experiencing any body aches?",
                "Have you noticed any changes in your appetite?",
                "Are you feeling more stressed than usual?",
                "Have you been in contact with anyone who is sick?"
            ]
        }

def generate_summary(symptoms, questions, answers):
    """
    Generates a health summary using an AI model based on symptoms and answers.
    """
    try:
        qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)])
        
        prompt = f"""
        A user provided the following information:
        Initial Symptoms: "{symptoms}"
        
        Follow-up Questions and Answers:
        {qa_pairs}

        Based on all this information, generate a concise, easy-to-understand health summary.
        The summary should be informative but not alarming.
        Start the summary with "Based on the information you provided...".
        IMPORTANT: At the end of the summary, you MUST include the following disclaimer exactly as written:
        "**Disclaimer:** This is not a medical diagnosis. This tool is for informational purposes only. Please consult with a healthcare professional for any health concerns."
        """

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant that provides clear, cautious health summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        print(f"Error calling AI for summary: {e}")
        return "We couldn't generate a summary at this time. Please try again later.\n\n**Disclaimer:** This is not a medical diagnosis. This tool is for informational purposes only. Please consult with a healthcare professional for any health concerns."
