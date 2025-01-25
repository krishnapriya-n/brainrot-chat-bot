from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with Nebius endpoint
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

def create_study_prompt(messages):
    """Create a prompt that guides the model to act as a tutor."""
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
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Create chat completion request
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            messages=create_study_prompt(message_history),
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