# generate_mcqs.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Retrieve the Gemini API key
GEMINI_API_KEY = os.getenv("QUIZ_API")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate MCQs using the Gemini model
def generate_mcqs(prompt, num_questions=10):
    # Start a chat session with the model
    chat = model.start_chat(
        history=[{"role": "user", "parts": f"Please generate {num_questions} multiple-choice questions (MCQs) related to the topic: {prompt}"},
                 {"role": "model", "parts": "Sure! I'll create the quiz questions."}]
    )
    
    # Send the prompt and get the response
    response = chat.send_message(f"Generate {num_questions} multiple-choice questions related to {prompt}. Include four options (A, B, C, D) and indicate the correct answer at the end of each question.")
    generated_text = response.text.strip()

    # Regex to extract questions, options, and correct answers
    pattern = r"(\d+\.)\s*(.*?)\n\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\n\s*\*\*Correct Answer:\s*(.*?)\*\*"
    
    # Find all matches using regex
    questions = []
    matches = re.findall(pattern, generated_text)

    # Extract and structure the data
    for match in matches:
        question = match[1].strip()  # Question text
        options = {
            'A': match[2].strip(),
            'B': match[3].strip(),
            'C': match[4].strip(),
            'D': match[5].strip(),
        }
        correct_answer = match[6].strip()  # Correct answer
        
        # Ensure correct_answer is a valid option key
        correct_answer_key = correct_answer.strip().upper()  # Ensure correct_answer is uppercase
        if correct_answer_key not in options:
            correct_answer_key = 'A'  # Default to A if not found, this is a fallback

        questions.append({
            'question': question,
            'options': options,
            'correct_answer': correct_answer_key
        })

    return questions[:num_questions]
