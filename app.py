import os      
import google.generativeai as genai
import streamlit as st
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
    # print(response)
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

# Streamlit-based quiz game
def quiz_game():
    st.title("Quiz Game")
    st.write("Welcome! Generate multiple-choice quiz questions on a topic of your choice.")

    # Input field for topic
    field = st.text_input("Enter the topic for the quiz (e.g., 'Science', 'History'):", key="topic_input")

    # Button to generate questions
    if st.button("Generate Quiz"):
        if field.strip():
            st.write("Generating questions, please wait...")

            # Generate MCQs from the Gemini model
            mcqs = generate_mcqs(field)
            st.session_state['questions'] = mcqs
            st.session_state['current_question'] = 0
            st.session_state['score'] = 0
            st.session_state['user_answers'] = {}  # Initialize user answers
        else:
            st.warning("Please enter a topic.")

    # Display one question at a time
    if 'questions' in st.session_state:
        questions = st.session_state['questions']
        current_question = st.session_state['current_question']
        
        if current_question < len(questions):
            question_data = questions[current_question]
            question_text = question_data['question']
            options = question_data['options']
            correct_answer_key = question_data['correct_answer']
            
            # Display the current question
            st.write(f"**Question {current_question + 1}:** {question_text}")

            # Reset user answer to None when the question changes
            if f"answer_{current_question}" not in st.session_state:
                st.session_state[f"answer_{current_question}"] = None

            # Display multiple-choice options to the user
            user_answer = st.radio(f"Choose your answer for Question {current_question + 1}:",
                                   list(options.values()), key=f"answer_{current_question}")

            # Button to submit the answer for the current question
            if st.button("Submit Answer", key=f"submit_{current_question}"):
                # Check if the user has selected an answer
                if user_answer is None:
                    st.warning("Please select a valid option before submitting!")
                else:
                    # Check if the answer is correct
                    if user_answer == options[correct_answer_key]:
                        st.success("Correct!")
                        st.session_state['score'] += 1
                    else:
                        st.error(f"Incorrect. The correct answer was: {options[correct_answer_key]}")

                    # Move to the next question
                    st.session_state['current_question'] += 1

        # After all questions are answered, display the score
        if current_question >= len(questions):
            st.write("Quiz Completed!")
            st.write(f"Your final score: {st.session_state['score']}/{len(questions)}")
            st.session_state.clear()  # Clear session state to reset the quiz

# Run the Streamlit app
if __name__ == "__main__":
    quiz_game()
