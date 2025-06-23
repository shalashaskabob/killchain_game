from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# In-memory game state
game_state = {
    "teams": [],
    "current_stage": 0,
    "current_turn_index": 0,
    "game_started": False,
    "processing_guess": False
}

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
    # Reset game state for a new session
    global game_state
    game_state = {
        "teams": [], "current_stage": 0, 
        "current_turn_index": 0, "game_started": False,
        "processing_guess": False
    }
    return render_template('setup.html')

@app.route('/setup', methods=['POST'])
def setup():
    num_teams = int(request.form['teams'])
    return render_template('name_teams.html', num_teams=num_teams)

@app.route('/start_game', methods=['POST'])
def start_game():
    game_state["teams"] = []
    for i in range(int(request.form['num_teams'])):
        team_name = request.form[f'team_{i}']
        game_state["teams"].append({"name": team_name, "score": 0})
    
    game_state["current_stage"] = 0
    game_state["current_turn_index"] = 0
    game_state["game_started"] = True
    
    # Notify all clients that the game has started
    socketio.emit('game_started')
    return redirect(url_for('game'))

@app.route('/game')
def game():
    if not game_state["game_started"]:
        return redirect(url_for('index'))
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    if game_state["game_started"]:
        emit('game_update', get_game_view())

@socketio.on('submit_guess')
def handle_guess(data):
    if not game_state["game_started"] or game_state["processing_guess"]:
        return

    game_state["processing_guess"] = True
    try:
        user_guess = data['guess'].strip()
        correct_stage = kill_chain[game_state["current_stage"]]['name']
        current_team = game_state["teams"][game_state["current_turn_index"]]

        if user_guess.lower() == correct_stage.lower():
            current_team["score"] += 1
            game_state["current_stage"] += 1
            emit('guess_result', {'correct': True, 'team': current_team['name']}, broadcast=True)
            
            if game_state["current_stage"] >= len(kill_chain):
                emit('game_over', {"winner": current_team['name'], "teams": game_state["teams"]}, broadcast=True)
                game_state["game_started"] = False
                return
        else:
            emit('guess_result', {'correct': False, 'team': current_team['name']}, broadcast=True)

        # Advance to the next team's turn
        game_state["current_turn_index"] = (game_state["current_turn_index"] + 1) % len(game_state["teams"])
        
        socketio.sleep(2) 
        emit('game_update', get_game_view(), broadcast=True)
    finally:
        game_state["processing_guess"] = False

def get_game_view():
    view = {
        "teams": game_state["teams"],
        "stage": kill_chain[game_state["current_stage"]],
        "progress": f"Stage {game_state['current_stage'] + 1}/{len(kill_chain)}",
        "current_turn": game_state["teams"][game_state["current_turn_index"]]["name"]
    }
    return view

@app.route('/win')
def win():
    # This route is now mostly handled by game_over socket event
    # but we can keep a simple win page as a fallback or for direct navigation
    return render_template('win.html', teams=game_state.get("teams", []))

if __name__ == '__main__':
    socketio.run(app, debug=True) 