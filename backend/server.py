from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Hardcoded API key (use only for testing or small-scale projects)
API_KEY = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDExMTkwNjM3MTE1NTUyMTEwNDkxMyIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTg5NTU1ODU2NiwidXVpZCI6IjdlMTQ1YjM0LTdjNjItNDgwNi05MWQ0LWUyNTJkNjhmYjgzYyIsIm5hbWUiOiJVbm5hbWVkIGtleSIsImV4cGlyZXNfYXQiOiIyMDMwLTAxLTI1VDA4OjAyOjQ2KzAwMDAifQ.YI53577RIQkzszQUjCThKCo_R3iuRDFdHeWKoR09rK0"

# Initialize OpenAI client with Nebius endpoint
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=API_KEY
)

def create_study_prompt(messages, mode="tutor"):
    """Create a prompt based on the selected mode."""
    if mode == "rubber_duck":
        system_prompt = """You are a curious and engaging learning companion in rubber duck mode. Your role is to help users learn by having them explain concepts to you. Ask thoughtful, probing questions that help users identify gaps in their understanding. Show genuine interest in their explanations and gently point out any misconceptions. Keep the tone friendly and encouraging.

Key behaviors:
1. Ask clarifying questions about concepts the user explains
2. Request examples to test understanding
3. Point out potential gaps or inconsistencies respectfully
4. Encourage deeper thinking with "what if" scenarios
5. Validate correct understanding with enthusiasm
6. Keep the conversation flowing naturally

Example interaction:
User: "Let me explain how a for loop works..."
Assistant: "I'd love to learn about for loops from you! As you explain, could you give me a simple example of when you'd use one?"
"""
    else:  # tutor mode
        system_prompt = """You're a Conversational Tutor with a knack for making learning feel like a fun, casual chat. Instead of dry, textbook definitions, break down topics in a way that's easy to understand and entertaining. Use relatable, fun analogies and keep the tone light and friendly. For example, when explaining electricity, you might say, 'Electricity's like the life of the party—flowing through wires and keeping things lit! When it stops, the vibe's gone, and everyone's just waiting for the fun to come back.' The goal is to make learning feel like a conversation, not a lecture!"""
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    
    for msg in messages:
        if msg.startswith("You: "):
            formatted_messages.append({"role": "user", "content": msg[5:]})
        elif msg.startswith("Bot: "):
            formatted_messages.append({"role": "assistant", "content": msg[5:]})
    
    return formatted_messages

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        message_history = data.get('history', [])
        mode = data.get('mode', 'tutor')  # Default to tutor mode if not specified
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Create chat completion request
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            messages=create_study_prompt(message_history, mode),
            temperature=0.6,
            max_tokens=512,
            top_p=0.9
        )
        
        # Log the interaction
        print(f"User: {user_message}")
        print(f"Bot: {completion.choices[0].message.content}")

        return jsonify({
            'response': completion.choices[0].message.content
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
