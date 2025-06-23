from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from app.questions import get_shuffled_questions

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory game state
game_state = {
    "teams": [],
    "questions": [],
    "current_question_index": 0,
    "current_turn_index": 0,
    "game_started": False,
    "processing_guess": False
}

def reset_game_state():
    """Resets the game to its initial state for a new game."""
    global game_state
    game_state = {
        "teams": [],
        "questions": get_shuffled_questions(),
        "current_question_index": 0,
        "current_turn_index": 0,
        "game_started": False,
        "processing_guess": False
    }

@app.route('/')
def index():
    reset_game_state()
    return render_template('setup.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    # Keep the shuffled questions but reset teams and progress
    teams = []
    for i in range(int(request.form['num_teams'])):
        team_name = request.form[f'team_{i}']
        teams.append({"name": team_name, "score": 0})
    
    game_state.update({
        "teams": teams,
        "current_question_index": 0,
        "current_turn_index": 0,
        "game_started": True,
        "processing_guess": False
    })
    
    # Notify all clients that the game has started
    socketio.emit('game_started')
    return redirect(url_for('game'))

@app.route('/game')
def game():
    if not game_state.get("game_started"):
        return redirect(url_for('index'))
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    if game_state.get("game_started"):
        emit('game_update', get_game_view())

@socketio.on('new_game')
def handle_new_game():
    reset_game_state()
    # Tell all clients to go back to the setup screen
    emit('redirect_to_setup', broadcast=True)

@socketio.on('submit_guess')
def handle_guess(data):
    if not game_state["game_started"] or game_state["processing_guess"]:
        return

    game_state["processing_guess"] = True
    try:
        user_guess = data['guess'].strip()
        correct_answer = game_state["questions"][game_state["current_question_index"]]["answer"]
        current_team = game_state["teams"][game_state["current_turn_index"]]

        if user_guess.lower() == correct_answer.lower():
            current_team["score"] += 1
            emit('guess_result', {'correct': True, 'team': current_team['name']}, broadcast=True)
            
            if current_team["score"] >= 10:
                emit('game_over', {"winner": current_team['name'], "teams": game_state["teams"]}, broadcast=True)
                game_state["game_started"] = False
                return
        else:
            emit('guess_result', {'correct': False, 'team': current_team['name']}, broadcast=True)

        # Advance to the next team's turn first
        game_state["current_turn_index"] = (game_state["current_turn_index"] + 1) % len(game_state["teams"])
        # Then advance the question
        game_state["current_question_index"] += 1

        socketio.sleep(2) 
        emit('game_update', get_game_view(), broadcast=True)
    finally:
        game_state["processing_guess"] = False

def get_game_view():
    """Constructs the data payload for the frontend."""
    # Ensure we don't go out of bounds if questions run out
    q_index = game_state['current_question_index'] % len(game_state['questions'])
    
    view = {
        "teams": game_state["teams"],
        "question": game_state["questions"][q_index]["description"],
        "question_number": game_state["current_question_index"] + 1,
        "current_turn": game_state["teams"][game_state["current_turn_index"]]["name"]
    }
    return view

if __name__ == '__main__':
    socketio.run(app, debug=True) 