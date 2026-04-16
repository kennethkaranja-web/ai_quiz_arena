from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for sessions

# Full 25-question quiz
questions = [
    {"id": 1, "question": "What best describes prompt engineering?",
     "options": ["A. Writing code for AI systems", "B. Teaching AI new data", "C. Automating tasks without review", "D. Giving clear, structured instructions to AI"],
     "answer": "D"},
    {"id": 2, "question": "Why do vague prompts often lead to weak AI outputs?",
     "options": ["A. AI tools ignore short prompts", "B. Vague prompts limit context and direction", "C. AI prefers technical language", "D. AI cannot process incomplete sentences"],
     "answer": "B"},
    {"id": 3, "question": "Which of these is an example of a strong prompt?",
     "options": ["A. Write something", "B. Tell me about history", "C. Summarize the causes of World War I in 3 bullet points", "D. Explain science"],
     "answer": "C"},
    {"id": 4, "question": "What is the benefit of specifying format in a prompt?",
     "options": ["A. AI ignores format", "B. It helps AI structure the output clearly", "C. It reduces accuracy", "D. It confuses the AI"],
     "answer": "B"},
    {"id": 5, "question": "Why might you include examples in a prompt?",
     "options": ["A. To confuse the AI", "B. To guide the AI toward the desired style or tone", "C. To reduce creativity", "D. To shorten the response"],
     "answer": "B"},
    {"id": 6, "question": "What does 'role prompting' mean?",
     "options": ["A. Assigning the AI a perspective or identity", "B. Giving AI random tasks", "C. Limiting AI vocabulary", "D. Removing context"],
     "answer": "A"},
    {"id": 7, "question": "Why is context important in prompts?",
     "options": ["A. It helps AI generate relevant answers", "B. It reduces accuracy", "C. It makes prompts shorter", "D. It confuses AI"],
     "answer": "A"},
    {"id": 8, "question": "What is 'chain-of-thought prompting'?",
     "options": ["A. Asking AI to guess", "B. Guiding AI to explain reasoning step by step", "C. Limiting AI to one word", "D. Removing logic"],
     "answer": "B"},
    {"id": 9, "question": "Which prompt is most likely to yield a creative story?",
     "options": ["A. Write a story", "B. Tell me something", "C. Write a 200-word fantasy story about a dragon who learns math", "D. Explain math"],
     "answer": "C"},
    {"id": 10, "question": "What happens if you ask AI to 'be concise'?",
     "options": ["A. It writes longer answers", "B. It ignores the request", "C. It produces shorter, focused responses", "D. It stops working"],
     "answer": "C"},
    {"id": 11, "question": "Why might you use step-by-step instructions in a prompt?",
     "options": ["A. To confuse AI", "B. To guide AI through complex tasks", "C. To reduce accuracy", "D. To shorten responses"],
     "answer": "B"},
    {"id": 12, "question": "What is the risk of overly broad prompts?",
     "options": ["A. AI gives generic or irrelevant answers", "B. AI becomes more accurate", "C. AI stops responding", "D. AI ignores the prompt"],
     "answer": "A"},
    {"id": 13, "question": "What does 'temperature' control in AI outputs?",
     "options": ["A. Creativity/randomness of responses", "B. The length of answers", "C. The accuracy of facts", "D. The speed of response"],
     "answer": "A"},
    {"id": 14, "question": "Why might you ask AI to 'explain like I’m five'?",
     "options": ["A. To confuse AI", "B. To simplify complex topics", "C. To reduce accuracy", "D. To make responses longer"],
     "answer": "B"},
    {"id": 15, "question": "What is the advantage of specifying audience in a prompt?",
     "options": ["A. AI ignores audience", "B. It tailors the response to the intended reader", "C. It reduces accuracy", "D. It confuses AI"],
     "answer": "B"},
    {"id": 16, "question": "What is 'few-shot prompting'?",
     "options": ["A. Giving AI no examples", "B. Providing a few examples to guide output", "C. Limiting AI to one word", "D. Removing context"],
     "answer": "B"},
    {"id": 17, "question": "Why might you use bullet points in a prompt?",
     "options": ["A. To confuse AI", "B. To structure the response clearly", "C. To reduce accuracy", "D. To shorten responses"],
     "answer": "B"},
    {"id": 18, "question": "What is the benefit of iterative prompting?",
     "options": ["A. Refining outputs by adjusting prompts step by step", "B. Confusing AI", "C. Reducing accuracy", "D. Making prompts shorter"],
     "answer": "A"},
    {"id": 19, "question": "Why might you ask AI to 'show reasoning'?",
     "options": ["A. To confuse AI", "B. To see how AI arrived at its answer", "C. To reduce accuracy", "D. To shorten responses"],
     "answer": "B"},
    {"id": 20, "question": "What is the risk of asking AI for opinions?",
     "options": ["A. AI may generate biased or subjective content", "B. AI becomes more accurate", "C. AI stops responding", "D. AI ignores the prompt"],
     "answer": "A"},
    {"id": 21, "question": "Why might you specify word count in a prompt?",
     "options": ["A. To confuse AI", "B. To control the length of the response", "C. To reduce accuracy", "D. To make responses longer"],
     "answer": "B"},
    {"id": 22, "question": "What is 'zero-shot prompting'?",
     "options": ["A. Giving AI no examples and expecting it to generalize", "B. Providing many examples", "C. Limiting AI to one word", "D. Removing context"],
     "answer": "A"},
    {"id": 23, "question": "Why might you ask AI to 'use analogies'?",
     "options": ["A. To confuse AI", "B. To make explanations more relatable", "C. To reduce accuracy", "D. To shorten responses"],
     "answer": "B"},
    {"id": 24, "question": "What is the benefit of combining role + task in a prompt?",
     "options": ["A. AI ignores roles", "B. It guides AI to respond in a specific way", "C. It reduces accuracy", "D. It confuses AI"],
     "answer": "B"},
    {"id": 25, "question": "What is the ultimate goal of prompt engineering?",
     "options": ["A. To confuse AI", "B. To maximize useful, accurate, and creative outputs", "C. To reduce AI accuracy", "D. To train AI models"],
     "answer": "B"}
]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    session['username'] = username
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    results = []
    for q in questions:
        user_answer = request.form.get(f"q{q['id']}")
        correct_answer = q['answer']
        is_correct = (user_answer == correct_answer)
        if is_correct:
            score += 1
        results.append({
            "id": q['id'],
            "question": q['question'],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    username = session.get('username', 'Anonymous')

    # Save score to file
    with open("leaderboard.txt", "a") as f:
        f.write(f"{username},{score}\n")

    # Reload leaderboard from file
    leaderboard = []
    with open("leaderboard.txt", "r") as f