from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
# Đặt API key Gemini ở đây hoặc qua biến môi trường
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBTiQUpuxVJx_xROaZeEH6Zg7ZNSuB0V1s")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('/api/lookup', methods=['POST'])
def lookup():
    data = request.get_json()
    phonetic = data.get('phonetic', '')
    if not phonetic:
        return jsonify({'error': 'No phonetic provided'}), 400
    prompt = f"Từ tiếng Anh nào có phiên âm {phonetic}? Trả lời bằng đúng một từ duy nhất."
    try:
        response = model.generate_content(prompt)
        word = response.text.strip()
        return jsonify({'word': word})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
