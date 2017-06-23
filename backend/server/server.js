const express = require('express');
const cors = require('cors');
var app = express();

app.use(cors({
	allowedOrigins: ['http://localhost:3000']
}));

app.get('/api/login/init', function (req, res) {
	res.send("hiya!");

	//this will log in terminal, not in console. this was working for me so we just handle logic here

	/*TODO 
		this will receive access token, go to fb api, query likes, query pages that have category 'articles',
		go through each page to see if the user has liked any specific articles (recently), then send links to
		backend 
	*/ 
	console.log("lol");
}) 

app.listen(3333, function() { 
	console.log("server started on port 3333")
});