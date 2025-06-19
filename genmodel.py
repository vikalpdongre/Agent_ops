import os
import google.generativeai as genai
from flask import jsonify

# Ensure your API key is set up
# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def analyze_resume_jd(resume_text, jd_text):
    if not resume_text or not jd_text:
        return jsonify({"error": "Both resume and job description are required"}), 400

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use the appropriate model
    except Exception as e:
        return jsonify({"error": f"Failed to load model: {e}"}), 500

    print(f"Model: {model}")

    prompt = f"Compare this resume and job description:\nResume:\n{resume_text}\n\nJob Description:\n{jd_text}\nProvide a match score and key skill highlights."

    try:
        response = model.generate_content(prompt)
        print(f"Response:", response)
    except Exception as e:
        return jsonify({"error": f"Error generating content from the model: {e}"}), 500

    if not response:
        return jsonify({"error": "No response object received from the model."}), 500

    # Check for prompt feedback and block reasons first
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        return jsonify({"error": f"Prompt was blocked by the model: {response.prompt_feedback.block_reason.name}"}), 400 # .name to get string representation

    # Check if there are any candidates and if the first candidate has text
    if not response.candidates or not response.candidates[0].content.parts[0].text:
        # If no candidates or no text, check the finish reason for more details
        if response.candidates and response.candidates[0].finish_reason:
            return jsonify({"error": f"Model did not return complete content. Finish reason: {response.candidates[0].finish_reason.name}"}), 500
        else:
            return jsonify({"error": "Model response is empty or malformed."}), 500

    return jsonify({"analysis": response.candidates[0].content.parts[0].text}), 200
