const execSync = require("child_process").execSync;
const express = require("express");
const cors = require("cors");
const app = express();
const port = 3000;

app.use(cors());

const getPy = async (text = "") => {
  const result = execSync(`python3 zh_change.py ${text}`);
  return result.toString("utf8");
};

app.get("/", (req, res) => {
  const { str } = req.query;
  const result = getPy(str);
  result.then((result) => res.json(JSON.parse(result.replace(/'/g, '"'))));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
