const express = require('express');
const cors = require('cors');
var app = express();

app.use(cors({
	allowedOrigins: ['http://localhost:3000']
}));

app.get('/api/login/init', function (req, res) {
	res.send("hiya!");
	console.log("lol");
}) 

app.listen(3333, function() { 
	console.log("server started on port 3333")
});