from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# template 
template = """"
Answer the following question:
Here is a conversation history: {context}
Question: {question}
Answer: 
"""

app = Flask(__name__)

# Initialize the chatbot with the llama3.2:1b model
def initialize_chatbot():
    model = OllamaLLM(model="llama3.2:1b")
    prompt = ChatPromptTemplate.from_template(template)
    chain =  prompt | model
    return chain

# Function to handle user queries
def handle_query(user_input, chain):
    context = {}
    if user_input.lower():
        result = chain.invoke({"context" : context , "question": user_input})
        context = f"\n User : {user_input}\n AI: {result}"
        return {"response": str(result)}
    else:
        return {"error": "No input provided"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    model = initialize_chatbot()
    response = handle_query(user_input, model)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
