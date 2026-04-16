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
    # ... include all 25 questions here exactly as before ...
    {"id": 25, "question": "What is the ultimate goal of prompt engineering?",
     "options": ["A. To confuse AI", "B. To maximize useful, accurate, and creative outputs", "C. To reduce AI accuracy", "D. To train AI models"],
     "answer": "B"}
]

# Leaderboard storage
leaderboard = []  # will store (username, score)

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
    leaderboard.clear()
    with open("leaderboard.txt", "r") as f:
        for line in f:
            name, s = line.strip().split(",")
            leaderboard.append((name, int(s)))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    return render_template(
        'results.html',
        score=score,
        total=len(questions),
        results=results,
        leaderboard=leaderboard[:5]
    )
@app.route('/leaderboard')
def show_leaderboard():
    # Reload leaderboard from file to ensure it's up to date
    leaderboard_data = []
    try:
        with open("leaderboard.txt", "r") as f:
            for line in f:
                name, s = line.strip().split(",")
                leaderboard_data.append((name, int(s)))
    except FileNotFoundError:
        pass

    leaderboard_data.sort(key=lambda x: x[1], reverse=True)

    return render_template('leaderboard.html', leaderboard=leaderboard_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
