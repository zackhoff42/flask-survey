from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
    """Renders the root route, displaying the survey title and instructions."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('root.html', title=title, instructions=instructions)

@app.route('/thank-you')
def show_thanks_page():
    """Displays thank you page if all questions have been answered."""
    
    return render_template('thank-you.html')

@app.route('/questions/<int:id>')
def show_question(id):
    survey_question = satisfaction_survey.questions[id]
    question = survey_question.question
    choices = survey_question.choices

    if responses == None:
        return redirect('/')
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    
    if len(responses) != id:
        flash(f'Invalid question id: {id}')
        return redirect(f'/questions/{len(responses)}')

    return render_template('/questions.html', question=question, choices=choices)

@app.route('/answer', methods=['POST'])
def add_response():
    response = request.form['response']
    responses.append(response)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    
    return redirect(f'/questions/{len(responses)}')