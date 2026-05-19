import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

def clean_json(text: str):
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found")

    json_text = text[start:end + 1]

    while json_text.count("{") < json_text.count("}"):
        json_text = json_text[:-1]

    return json.loads(json_text)


def calculator(expression: str) -> str:
    try:
        allowed = "0123456789+-*/(). %"
        if not all(char in allowed for char in expression):
            return "Invalid expression"
        return str(eval(expression))
    except Exception as e:
        return str(e)


def call_ollama(messages):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        },
        timeout=300
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


user_question = "Explain what 25% of 18400 means"

messages = [
    {
        "role": "system",
        "content": """
You are an AI agent controller.

Return EXACTLY ONE JSON object.
Do not include explanation.
Do not include markdown.
Do not include more than one JSON object.

For math questions, return:
{"action": "calculator", "input": "0.25 * 18400"}

For non-math questions, return:
{"action": "final", "answer": "your answer"}

Rules:
- input must be a plain math expression string
- never put JSON inside input
- never calculate math yourself
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]

decision_text = call_ollama(messages)

print("MODEL DECISION:")
print(decision_text)

try:
   
    decision = clean_json(decision_text)
except:
    print("\nERROR: Model did not return valid JSON")
    exit()

if decision["action"] == "calculator":
    result = calculator(decision["input"])

    final_messages = messages + [
        {"role": "assistant", "content": decision_text},
        {"role": "user", "content": f"Result is {result}. Give final answer."}
    ]

    final_answer = call_ollama(final_messages)

    print("\nFINAL ANSWER:")
    try:
     final_decision = clean_json(final_answer)
     print(final_decision["answer"])
    except:
     print(final_answer)

else:
    print("\nFINAL ANSWER:")
    print(decision["answer"])