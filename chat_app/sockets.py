# Импортировать socketio-сервер
from app.settings import socketio_server
from flask_socketio import join_room,leave_room
# Написать обработчик события message
@socketio_server.on("message")
def handle_message_send(data):
    chat_id = data["chat_id"]
    socketio_server.emit("message", data,to = f"room_{chat_id}")
    print(data)

@socketio_server.on("join_room")
def handle_room_join(data):
    chat_id = data["chat_id"]
    join_room(f"room_{chat_id}")
    print(data)

# socketio_server.on() - обрабатывает socketio-событие
# socketio_server.emit() - отправляет socketio-событие
