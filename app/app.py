from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Cyber Kill Chain Stages
kill_chain = [
    {"name": "Reconnaissance", "description": "Gathering information about the target."},
    {"name": "Weaponization", "description": "Creating a malicious payload to send to the target."},
    {"name": "Delivery", "description": "Transmitting the weapon to the target."},
    {"name": "Exploitation", "description": "Triggering the weapon to exploit a vulnerability."},
    {"name": "Installation", "description": "Installing malware on the target system."},
    {"name": "Command & Control", "description": "Establishing a command channel to the target."},
    {"name": "Actions on Objectives", "description": "Performing the ultimate goal of the attack."}
]

@app.route('/')
def index():
    if 'score' not in session:
        session['score'] = 0
        session['current_stage'] = 0
    
    current_stage_data = kill_chain[session['current_stage']]
    return render_template('index.html', stage=current_stage_data)

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = request.form['stage'].strip()
    correct_stage = kill_chain[session['current_stage']]['name']

    if user_guess.lower() == correct_stage.lower():
        session['score'] += 1
        session['current_stage'] += 1
        if session['current_stage'] >= len(kill_chain):
            return redirect(url_for('win'))
    
    return redirect(url_for('index'))

@app.route('/win')
def win():
    score = session.get('score', 0)
    session.clear()
    return render_template('win.html', score=score)

if __name__ == '__main__':
    app.run(debug=True) 