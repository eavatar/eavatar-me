

ava.wsconnection =  {

    url: "ws://127.0.0.1:5080/ws",
    socket: null,

    open: function() {
        this.socket = new WebSocket(this.url)
        this.socket.onopen = this.on_open
        this.socket.onclose = this.on_close
        this.socket.onmessage = this.on_message
    },

    send: function(msg) {
        console.log("Send message:", msg)
        this.socket.send(msg)
    },

    close: function() {
        if(this.socket === undefined) {
            return
        }

        this.socket.close()
    },

    on_open: function(event) {
        console.log("Websocket connected.")
        this.send("Hi")
    },

    on_message: function(event) {
        console.log("Received msg:", event.data)
    },

    on_close: function(event) {
    },

    on_error: function(event) {
        console.log("Websocket error:", event)
    }
};