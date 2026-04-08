import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/docs")
def docs():
    return render_template("landing.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    business_type = data.get("business_type", "dental clinic")
    caller_message = data.get("caller_message", "")
    tone = data.get("tone", "professional and friendly")
    services = data.get("services", "")

    prompt = f"""You are an AI receptionist/voice agent for a {business_type}. Your tone is {tone}.

The business offers these services: {services if services else 'general services typical for a ' + business_type}

A caller says: "{caller_message}"

Respond exactly as a world-class receptionist would. Be warm, helpful, and efficient. Your response should:

1. Greet or acknowledge the caller naturally
2. Address their specific request or question
3. Offer to help with scheduling, information, or routing
4. Confirm next steps clearly

Format your response as:

RECEPTIONIST RESPONSE:
[Your natural spoken response to the caller]

DETECTED INTENT:
[What the caller wants: appointment, information, complaint, transfer, etc.]

SUGGESTED ACTIONS:
[Bullet list of CRM/calendar actions this would trigger in a real system]

FOLLOW-UP PROMPT:
[What the receptionist should ask next if the conversation continues]"""

    try:
        message = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"result": message.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5038)
