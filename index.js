const execSync = require("child_process").execSync;
const express = require("express");
const cors = require("cors");
const { io } = require("socket.io-client");

const socket = io("http://localhost:3000");

socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});

socket.on('connect', function (socket) {
  console.log('Connected!');
});

let receivedMsg = null

socket.on('my response', function(msg) {
  console.log("my response", msg)
  receivedMsg = msg
});

// setTimeout(() => {
//   socket.emit("my_message", "我們好好丫")
// }, 2000)

const app = express();
const port = 4320;

app.use(cors());

app.get("/", async (req, res) => {
  const { str } = req.query;

  // 清空
  receivedMsg = null

  // 發送到 python
  socket.emit("my_message", str)

  // 等待 python 處理完返回
  while(receivedMsg === null) {
    await new Promise(resolve => {
      setTimeout(() => {
        resolve()
      }, 100)
    })
  }

  res.json(receivedMsg)
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
