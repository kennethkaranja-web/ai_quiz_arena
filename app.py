from flask import Flask, render_template, request

app = Flask(__name__)

# Full 25-question quiz
questions = [
    {"id": 1, "question": "What best describes prompt engineering?", 
     "options": ["Writing code for AI systems", "Teaching AI new data", "Automating tasks without review", "Giving clear, structured instructions to AI"], 
     "answer": "D"},
    {"id": 2, "question": "Why do vague prompts often lead to weak AI outputs?", 
     "options": ["AI tools ignore short prompts", "Vague prompts limit context and direction", "AI prefers technical language", "AI cannot process incomplete sentences"], 
     "answer": "B"},
    {"id": 3, "question": "Which of these is an example of a strong prompt?", 
     "options": ["Tell me something", "Explain quantum computing in simple terms", "Do it", "Write stuff"], 
     "answer": "B"},
    {"id": 4, "question": "What is the main goal of prompt engineering?", 
     "options": ["To confuse AI", "To maximize useful outputs", "To train AI models", "To reduce AI accuracy"], 
     "answer": "B"},
    {"id": 5, "question": "Which prompt is likely to give the most detailed answer?", 
     "options": ["Explain photosynthesis", "Explain photosynthesis step by step for a 10-year-old", "Plants", "Tell me science"], 
     "answer": "B"},
    {"id": 6, "question": "What happens if you give contradictory instructions in a prompt?", 
     "options": ["AI ignores them", "AI may produce inconsistent results", "AI always chooses the first instruction", "AI refuses to answer"], 
     "answer": "B"},
    {"id": 7, "question": "Which of these is NOT part of good prompt design?", 
     "options": ["Clarity", "Specificity", "Ambiguity", "Structure"], 
     "answer": "C"},
    {"id": 8, "question": "Why is context important in prompts?", 
     "options": ["It makes AI slower", "It helps AI generate relevant answers", "It confuses AI", "It reduces accuracy"], 
     "answer": "B"},
    {"id": 9, "question": "What does 'zero-shot prompting' mean?", 
     "options": ["AI is trained with zero data", "AI answers without examples", "AI refuses to answer", "AI generates random text"], 
     "answer": "B"},
    {"id": 10, "question": "What does 'few-shot prompting' mean?", 
     "options": ["AI is trained with millions of examples", "AI is given a few examples in the prompt", "AI ignores examples", "AI generates few words"], 
     "answer": "B"},
    {"id": 11, "question": "Which prompt is most likely to confuse AI?", 
     "options": ["Summarize this article in 3 bullet points", "Write a poem about the moon", "Tell me something about something", "Explain gravity"], 
     "answer": "C"},
    {"id": 12, "question": "What is chain-of-thought prompting?", 
     "options": ["Asking AI to show step-by-step reasoning", "Giving AI random instructions", "Training AI with chains", "Asking AI to think silently"], 
     "answer": "A"},
    {"id": 13, "question": "Why is specifying format useful in prompts?", 
     "options": ["It limits AI", "It ensures structured output", "It confuses AI", "It reduces accuracy"], 
     "answer": "B"},
    {"id": 14, "question": "Which of these is a bad prompt?", 
     "options": ["Write a 200-word essay on climate change", "Tell me stuff", "Explain Newton’s laws with examples", "Summarize the book in 5 bullet points"], 
     "answer": "B"},
    {"id": 15, "question": "What is the benefit of role-based prompting?", 
     "options": ["It makes AI slower", "It helps AI adopt a perspective", "It confuses AI", "It reduces accuracy"], 
     "answer": "B"},
    {"id": 16, "question": "Which of these prompts uses role-based prompting?", 
     "options": ["Explain AI", "As a teacher, explain AI to a student", "Tell me about AI", "AI stuff"], 
     "answer": "B"},
    {"id": 17, "question": "Why is iteration important in prompt engineering?", 
     "options": ["AI refuses to answer otherwise", "You refine prompts for better results", "It confuses AI", "It reduces accuracy"], 
     "answer": "B"},
    {"id": 18, "question": "What is the risk of overly long prompts?", 
     "options": ["AI ignores them", "AI may lose focus or misinterpret", "AI refuses to answer", "AI generates random text"], 
     "answer": "B"},
    {"id": 19, "question": "Which of these prompts is most likely to yield a creative story?", 
     "options": ["Tell me something", "Write a short story about a robot learning emotions", "Explain math", "Give me data"], 
     "answer": "B"},
    {"id": 20, "question": "What is the purpose of delimiters in prompts?", 
     "options": ["To confuse AI", "To separate instructions or text clearly", "To reduce accuracy", "To make AI slower"], 
     "answer": "B"},
    {"id": 21, "question": "Which of these is an example of a delimiter?", 
     "options": ["###", "AI", "Prompt", "Answer"], 
     "answer": "A"},
    {"id": 22, "question": "Why is testing prompts important?", 
     "options": ["To confuse AI", "To evaluate and improve outputs", "To reduce accuracy", "To make AI slower"], 
     "answer": "B"},
    {"id": 23, "question": "What is the main challenge in prompt engineering?", 
     "options": ["AI refuses to answer", "Balancing clarity, context, and creativity", "AI ignores prompts", "AI generates random text"], 
     "answer": "B"},
    {"id": 24, "question": "Which of these prompts is most likely to fail?", 
     "options": ["Explain the water cycle in 5 steps", "Tell me something", "Write a poem about love", "Summarize the article"], 
     "answer": "B"},
    {"id": 25, "question": "What is the ultimate goal of prompt engineering?", 
     "options": ["To confuse AI", "To maximize useful, accurate, and creative outputs", "To reduce AI accuracy", "To train AI models"], 
     "answer": "B"}
]

@app.route('/')
def index():
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
    return render_template('results.html', score=score, total=len(questions), results=results)

if __name__ == '__main__':
    app.run(debug=True)
