import os
from flask import Flask, request, render_template, jsonify
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Replace with your actual Mistral AI API key
MISTRAL_API_KEY = "8LLev8jl5CUHAwlF3uEh1vfpF0X0IDdo"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_logs():
    """Analyze uploaded log file using Mistral AI"""
    if 'logfile' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    log_file = request.files['logfile']

    if log_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Read the log content
        log_content = log_file.read().decode('utf-8')
        logger.info(f"Processing log file: {log_file.filename}, size: {len(log_content)} bytes")

        # Prepare the prompt for Mistral AI
        prompt = create_analysis_prompt(log_content)

        # Call Mistral API
        analysis_result = call_mistral_api(prompt)

        return jsonify({"result": analysis_result})

    except Exception as e:
        logger.error(f"Error analyzing logs: {str(e)}")
        return jsonify({"error": f"Error analyzing logs: {str(e)}"}), 500

def create_analysis_prompt(log_content):
    """Create a structured prompt for the LLM"""
    return f"""You are a Kubernetes troubleshooting expert. Analyze the following Kubernetes log content and:
1. What is the pod name? in which namespace it is present in?
2. Identify the specific error(s) present 
3. Classify the issue type (pod issue, node issue, configuration issue, or developer/application issue)
4. Explain the root cause in simple terms
5. Provide specific steps to solve the problem
6. Indicate whether this requires DevOps action or developer intervention
7. can the issue be resolved with pod restarts or scaling of pods?

Log content:
```
{log_content}
```

Format your response with clear headings for each section."""

def call_mistral_api(prompt):
    """Call Mistral AI API with the prepared prompt"""
    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-large-latest",  # Use appropriate model
            "messages": [
                {"role": "system", "content": "You are a Kubernetes troubleshooting expert who provides clear, concise, and accurate analysis of Kubernetes logs."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2  # Lower temperature for more focused responses
        }

        logger.info("Calling Mistral AI API")
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            # Extract the assistant's message content
            analysis = result["choices"][0]["message"]["content"]
            return analysis
        else:
            logger.error(f"API error: {response.status_code}, {response.text}")
            return f"Error from Mistral AI API: {response.status_code}, {response.text}"

    except Exception as e:
        logger.error(f"Exception when calling Mistral AI API: {str(e)}")
        return f"Error calling Mistral AI API: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)