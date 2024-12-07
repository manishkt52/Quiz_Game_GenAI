# main.py
import streamlit as st
from models.gemini_ai import generate_mcqs

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
