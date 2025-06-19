from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from  genmodel import analyze_resume_jd

os.environ["GOOGLE_API_KEY"] = "AIzaSyDQ43Zsp9rJRpg5GI_LvW6pw-vJWLGA-xI"  # Replace with your actual API key

genai.configure(api_key="AIzaSyDQ43Zsp9rJRpg5GI_LvW6pw-vJWLGA-xI")
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data['resume']
    jd_text = data['job_description']
    return analyze_resume_jd(resume_text, jd_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
