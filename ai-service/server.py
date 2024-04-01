from flask import Flask, jsonify, request, send_file, redirect
import requests
import base64
from dotenv import load_dotenv
import os
import httpx
import re
import asyncio

from openai import OpenAI

load_dotenv()
app = Flask(__name__)

client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# TO add your own grafana api key
grafana_api_key = 'glsa_QMv2lxVe9afG3ME5BoG0IFX8yKgVtdOP_06324b5c'

def escape_latex_characters(text):
    """Escapes LaTeX special characters in a given text."""
    # Mapping of LaTeX special characters to their escaped versions
    replacements = {
        "&": r"\&",
        "%": r"\%", # handled below separately
        "$": r"\$",
        "#": r"\#",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": "",
        "°C": r"$^\\circ$C",
        "(": r"\(",
        ")": r"\)",
        "-": " ", 
        "_": " ",
        "*": " ", 
    }
    
      # First, manually escape % signs that are not part of a LaTeX command or math mode
    text = re.sub(r'(?<!\\)%', r'\%', text)  # Escape % signs that do not have a preceding backslash
    
    for old, new in replacements.items():
        text = re.sub(re.escape(old), new.replace("\\", "\\\\"), text)
    
    return text

def replace_executive_summary(latex_file_path, new_summary):
    with open(latex_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    updated_content = content.replace("Summary of Dashboard.", new_summary)
    
    with open(latex_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def generate_pdf(grafana_url):
    try:
        response = requests.get(grafana_url)

        response.raise_for_status()

        temp_pdf_path = './iaq-report.pdf'
        with open(temp_pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        
        return send_file(temp_pdf_path, as_attachment=True)

    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

@app.route('/')
def test_route():
    return jsonify('Hello from ai-service!')

@app.route('/dashboardPanelsBase64', methods=['GET'])
def get_dashboard_panels_base64():
    dashboard_uid = request.args.get('dashboardUid')
    grafana_url = 'http://grafana:3000'
    panel_ids = ['1', '2', '3', '5', '6', '7', '8']

    async def fetch_image_base64(url):
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers={'Authorization': f'Bearer {grafana_api_key}'})
            return base64.b64encode(resp.content).decode('utf-8')

    async def gather_images():
        tasks = [fetch_image_base64(f"{grafana_url}/render/d-solo/{dashboard_uid}/iaq-report-dashboard?orgId=1&from=1708891975344&to=1711483975344&panelId={panel_id}&width=1000&height=500&tz=Asia%2FSingapore") for panel_id in panel_ids]
        return await asyncio.gather(*tasks)

    images_base64 = asyncio.run(gather_images())
    print('images_base64', images_base64)
    return jsonify(base64Images=images_base64)
    
@app.route('/get-dashboard-summary', methods=['GET'])
def get_dashboard_summary():
    images_service_url = 'http://localhost:5002/dashboardPanelsBase64'
    
    response = requests.get(images_service_url, params={'dashboardUid': 'bf902a40-1257-452b-99ae-3304c18e5824'})

    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve dashboard base64 images"}), 500
    
    base64_images = response.json()['base64Images']

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Can you generate a executive summary based on all the panel images? Please format symbol in their full abbrieviation, e.g. write 'percentage' for %, write 'degrees celsius' for °C, write 'relative humidity' for %RH etc.",
                }
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}} for base64_image in base64_images],
        }
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": messages,
        "max_tokens": 600
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    messageContent = response_json['choices'][0]['message']['content']

    # latex_file_path = '../templates/template.tex'
    latex_file_path = '/var/lib/ai-service/templates/template.tex'
        
    escaped_messageContent = escape_latex_characters(messageContent)
    print('escaped_messageContent', escaped_messageContent)

    replace_executive_summary(latex_file_path, escaped_messageContent)

    report_endpoint = f"http://grafana-reporter:8686/api/v5/report/bf902a40-1257-452b-99ae-3304c18e5824?apitoken={grafana_api_key}&template=template"
    report_response = requests.get(report_endpoint)

    print('report_response', report_response)
    
    if report_response.status_code == 200:
        print("Successfully called the report endpoint.")
        generate_pdf(report_endpoint)
    else:
        print(f"Failed to call the report endpoint. Status code: {report_response.status_code}")

    report_link = f"http://localhost:8686/api/v5/report/bf902a40-1257-452b-99ae-3304c18e5824?apitoken={grafana_api_key}&template=template"

    redirect(report_link)
    return jsonify(f"Success! Go to {report_link} to see your pdf report.")

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')

