from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import random
from questions import kill_chain_questions
from mitre_questions import mitre_attack_questions

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory game state
game_state = {}
processing_guess = False

def get_kill_chain_categories():
    return [
        "Reconnaissance", "Weaponization", "Delivery", "Exploitation", 
        "Installation", "Command & Control", "Actions on Objectives"
    ]

def get_mitre_attack_tactics():
    return [
        "Reconnaissance", "Resource Development", "Initial Access", "Execution", 
        "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access",
        "Discovery", "Lateral Movement", "Collection", "Command and Control", 
        "Exfiltration", "Impact"
    ]

def reset_game():
    global game_state, processing_guess
    game_state = {}
    processing_guess = False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/setup')
def setup():
    game_type = request.args.get('game_type', 'kill_chain')
    return render_template('setup.html', game_type=game_type)

@app.route('/name-teams', methods=['POST'])
def name_teams():
    num_teams = int(request.form['num_teams'])
    game_type = request.form['game_type']
    return render_template('name_teams.html', num_teams=num_teams, game_type=game_type)

@app.route('/start', methods=['POST'])
def start_game():
    global game_state
    reset_game()
    
    team_names = [request.form[f'team_{i}'] for i in range(int(request.form['num_teams']))]
    game_type = request.form['game_type']

    if game_type == 'mitre':
        questions = mitre_attack_questions
        categories = get_mitre_attack_tactics()
        question_key = 'tactic'
    else:
        questions = kill_chain_questions
        categories = get_kill_chain_categories()
        question_key = 'stage'
        
    random.shuffle(questions)

    game_state = {
        'teams': {name: 0 for name in team_names},
        'current_turn_index': 0,
        'questions': questions,
        'current_question_index': 0,
        'game_over': False,
        'winner': None,
        'game_type': game_type,
        'categories': categories,
        'question_key': question_key
    }
    return redirect(url_for('index'))

@app.route('/game')
def index():
    if not game_state:
        return redirect(url_for('home'))
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    if game_state:
        emit('game_state_update', {
            'teams': game_state.get('teams', {}),
            'current_turn': get_current_turn(),
            'current_question': get_current_question(),
            'game_over': game_state.get('game_over', False),
            'winner': game_state.get('winner', None),
            'categories': game_state.get('categories', [])
        })

@socketio.on('get_game_state')
def get_game_state():
    if game_state:
        emit('game_state_update', {
            'teams': game_state.get('teams', {}),
            'current_turn': get_current_turn(),
            'current_question': get_current_question(),
            'game_over': game_state.get('game_over', False),
            'winner': game_state.get('winner', None),
            'categories': game_state.get('categories', [])
        })

def get_current_question():
    if not game_state or 'questions' not in game_state or not game_state['questions']:
        return None
    q_index = game_state['current_question_index'] % len(game_state['questions'])
    return game_state['questions'][q_index]

def get_current_turn():
    if not game_state or 'teams' not in game_state or not game_state['teams']:
        return None
    team_names = list(game_state['teams'].keys())
    return team_names[game_state['current_turn_index']]

@socketio.on('submit_guess')
def handle_guess(data):
    global game_state, processing_guess
    if processing_guess:
        return

    processing_guess = True
    
    guess = data['guess']
    question_index = game_state['current_question_index']
    correct_answer = game_state['questions'][question_index][game_state['question_key']]
    
    current_team_name = get_current_turn()

    if guess.lower() == correct_answer.lower():
        game_state['teams'][current_team_name] += 1
        if game_state['teams'][current_team_name] >= 10:
            game_state['game_over'] = True
            game_state['winner'] = current_team_name
            emit('game_over', {"winner": current_team_name, "teams": game_state['teams']}, broadcast=True)
            return
        emit('guess_result', {'correct': True, 'team': current_team_name}, broadcast=True)
    else:
        emit('guess_result', {'correct': False, 'team': current_team_name}, broadcast=True)

    # Advance to the next team's turn first
    game_state['current_turn_index'] = (game_state['current_turn_index'] + 1) % len(game_state['teams'])
    # Then advance the question
    game_state['current_question_index'] += 1

    socketio.sleep(2) 
    emit('game_state_update', {
        'teams': game_state.get('teams', {}),
        'current_turn': get_current_turn(),
        'current_question': get_current_question(),
        'game_over': game_state.get('game_over', False),
        'winner': game_state.get('winner', None),
        'categories': game_state.get('categories', [])
    }, broadcast=True)
    
    processing_guess = False

@socketio.on('new_game')
def handle_new_game():
    reset_game()
    emit('redirect_to_home', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True) 