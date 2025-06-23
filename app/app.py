from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import random
import threading
from questions import kill_chain_questions
from mitre_questions import mitre_attack_questions

app = Flask(__name__)
socketio = SocketIO(app)

game_state = {}
game_lock = threading.Lock()
QUESTION_TIMER_SECONDS = 20

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
    global game_state
    game_state = {}

def advance_turn():
    """Advances the turn and question index."""
    if not game_state or game_state.get('game_over'):
        return

    game_state['current_turn_index'] = (game_state['current_turn_index'] + 1) % len(game_state['teams'])
    game_state['current_question_index'] += 1

def question_timer_expired(question_index):
    """
    This function is called after the timer runs out.
    It checks if the question is still the current one, and if so, advances the turn.
    """
    team_name_at_timeout = None
    should_update_clients = False

    with game_lock:
        if game_state and not game_state.get('game_over') and game_state.get('current_question_index') == question_index:
            team_name_at_timeout = get_current_turn()
            advance_turn()
            should_update_clients = True
    
    if should_update_clients:
        # Emit events outside the lock to avoid holding it during network I/O and sleeps
        socketio.emit('times_up', {'team': team_name_at_timeout})
        socketio.sleep(2)  # Give clients time to see the "time's up" message
        
        # Now, send the new state and start the next timer.
        with game_lock:
            send_game_state_update()
            if not game_state.get('game_over'):
                start_question_timer()

def start_question_timer():
    """Starts a background task that will trigger after the delay."""
    if not game_state.get('game_over'):
        current_question_index = game_state.get('current_question_index')
        socketio.start_background_task(question_timer_expired, current_question_index)

def send_game_state_update():
    """Emits a game state update to all clients."""
    if not game_state:
        return
    
    full_state = get_full_game_state()
    socketio.emit('game_state_update', full_state)

def get_full_game_state():
    """Constructs the complete game state for the client."""
    return {
        'teams': game_state.get('teams', {}),
        'current_turn': get_current_turn(),
        'current_question': get_current_question(),
        'game_over': game_state.get('game_over', False),
        'winner': game_state.get('winner', None),
        'categories': game_state.get('categories', []),
        'game_type': game_state.get('game_type', 'kill_chain')
    }

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
    with game_lock:
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
    # Don't start the timer here, redirecting to /game will trigger the first 'connect'
    return redirect(url_for('index'))

@app.route('/game')
def index():
    if not game_state:
        return redirect(url_for('home'))
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    with game_lock:
        if game_state:
            # Send the initial state, the client will request to start the timer
            emit('game_state_update', get_full_game_state())

@socketio.on('get_game_state_and_start_timer')
def get_game_state_and_start_timer():
    with game_lock:
        send_game_state_update()
        start_question_timer()

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
    guess_was_made = False
    with game_lock:
        if game_state and not game_state.get('game_over'):
            guess_was_made = True
            guess = data['guess']
            question_index = game_state['current_question_index']
            correct_answer = game_state['questions'][question_index][game_state['question_key']]
            current_team_name = get_current_turn()

            if guess.lower() == correct_answer.lower():
                game_state['teams'][current_team_name] += 1
                if game_state['teams'][current_team_name] >= 10:
                    game_state['game_over'] = True
                    game_state['winner'] = current_team_name
                socketio.emit('guess_result', {'correct': True, 'team': current_team_name})
            else:
                socketio.emit('guess_result', {'correct': False, 'team': current_team_name})

            if not game_state.get('game_over'):
                advance_turn()

    if guess_was_made:
        # Perform sleep and update outside the lock
        socketio.sleep(2)
        with game_lock:
            send_game_state_update()
            if not game_state.get('game_over'):
                start_question_timer()

@socketio.on('new_game')
def handle_new_game():
    with game_lock:
        reset_game()
    emit('redirect_to_home')

if __name__ == '__main__':
    socketio.run(app, debug=True) 