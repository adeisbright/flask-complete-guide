const selector = e => document.querySelector(e) 

const serverTag = selector("#serverMessage") 

serverTag.textContent = "This is a message from the server"