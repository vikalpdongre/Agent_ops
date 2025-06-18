from flask import Flask, request, jsonify
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data['resume']
    jd_text = data['job_description']

    prompt = f"Compare this resume and job description:\nResume:\n{resume_text}\n\nJob Description:\n{jd_text}\nProvide a match score and key skill highlights."
    response = genai.generate_text(prompt=prompt)

    return jsonify({"analysis": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
