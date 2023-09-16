import flask
import flask_socketio

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return flask.render_template('./index.html')

rooms = {'abc': {
    'name': 'abc',
    'member': [],
    'max_member_cnt': 4,
    'is_open': True,
}}

@socketio.on('enter_room')
def enter_room(data):
    room_id = data['roomID']
    username = data['username']
    print(room_id, username)

    if len(username) == 0:
        print('Error: username is empty')
        socketio.emit('error', {'error': 'username is empty'})
        return

    if room_id not in rooms:
        print('Error: room not found')
        socketio.emit('error', {'error': 'room not found'})
        return
    
    room = rooms[room_id]
    if not room['is_open']:
        print('Error: room is not open')
        socketio.emit('error', {'error': 'room is not open'})
        return
    
    room['member'].append(username)
    print(f"{username}さんが入室しました。")
    if len(room['member']) >= room['max_member_cnt']:
        print('部屋の定員に達しました')
        room['is_open'] = False
        socketio.emit('start_game', {
            'user_names': room['member']
        })
    
    # TODO: 規定の時間を超えてる場合は終了


if __name__ == '__main__':
    socketio.run(app)
