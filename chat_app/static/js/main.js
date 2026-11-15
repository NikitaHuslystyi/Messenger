let input_id = document.querySelector("#input-field")

const button = document.querySelector("#send-button")

const container = document.getElementById("message-container")

button.addEventListener("click", function() {
    console.log("Кнопка была нажата")

    let text = input_id.value
    let path_parts = window.location.pathname.split("/")
    let chat_id = path_parts[path_parts.length - 1]
    socket.emit("message", {message: text,chat_id : chat_id})
})


socket.on("message", (data) => {
    
    console.log(data)

    let messageText = data.message
    
    const paraghraph = document.createElement("p")
    // УКазать текст сообщения в параграфе
    paraghraph.textContent = messageText
    // Добавить параграф в container
    container.append(paraghraph)
    
})