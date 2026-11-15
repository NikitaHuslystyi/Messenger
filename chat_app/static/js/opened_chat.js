let path_parts = window.location.pathname.split("/")
let chat_id = path_parts[path_parts.length - 1]

socket.emit("join_room", {chat_id: chat_id})