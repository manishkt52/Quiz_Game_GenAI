from flask import Flask, request, jsonify
from models.gemini_ai import generate_mcqs

app = Flask(__name__)

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    """
    Endpoint to generate quiz questions based on a topic.
    Input: JSON with "topic" key.
    Output: JSON with a list of questions, options, and correct answers.
    """
    data = request.get_json()

    # Validate the input
    if not data or 'topic' not in data:
        return jsonify({"error": "Invalid request. 'topic' is required."}), 400
    
    topic = data['topic'].strip()
    if not topic:
        return jsonify({"error": "Topic cannot be empty."}), 400
    
    try:
        # Generate MCQs
        mcqs = generate_mcqs(topic)

        # Format the response
        response = {
            "topic": topic,
            "questions": mcqs
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle errors and return an appropriate response
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
