from flask import Flask, request, jsonify, render_template
from model_utils import model, tokenizer, device, evaluate
from chat_utils import append_chat_to_file, extract_increments, write_csv, git_push
import os

app = Flask(__name__)

# Immediately clear files
open("chat_output.txt", "w").close()
with open("movement_increments.csv", "w") as f:
    f.write("X,Y,Z\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    output = evaluate(model, tokenizer, user_input, device)

    append_chat_to_file(user_input, output)
    increments = extract_increments()
    write_csv(increments)

    try:
        git_push()
    except Exception as e:
        print("Git push failed:", e)

    return jsonify({"response": output})

if __name__ == "__main__":
    app.run(debug=True)
