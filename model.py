from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load GPT-2 model and tokenizer
model_name = "./trained_model"  # You can change to 'gpt2-medium', 'gpt2-large', etc.
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

# Optional: use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "")
    max_length = data.get("max_length",  100)

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    # Encode input and generate output
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=max_length, do_sample=True, top_k=50, top_p=0.95)

    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response_text})

@app.route('/')
def home():
    return "GPT-2 Flask API is running."

if __name__ == '__main__':
    app.run()
