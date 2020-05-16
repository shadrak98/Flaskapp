var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var db = require('./db');
var session = require('express-session');

var port = 3000;

var app = express();

//session
app.use(session({
  secret: 'finalyearg2',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: true }
}));

// view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

// bodyparser
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'templates')));

// app.get('/', function(req, res){
// 	res.render('index');
// });

app.get('/', function(req, res){
    db.query("SELECT * FROM Tasks",function(err, result){
    	if(err) throw err;
    	json_response = []
		for(i=0;i<result.length;i++){
			json_object = {}
			json_object["tasks"] = result[i].tasks
			json_response.push(json_object)
		}
    	console.log(json_response)

    	// console.log("result:"+JSON.stringify(result));
    	res.render('index',{
    		tasks: json_response
    	});
    });
});


app.post('/addtask', function(req, res){
	console.log(req.body);
	var task = req.body.myInput;
	console.log(task);
	db.query("INSERT INTO Tasks(tasks) VALUES(?)", [task], function(err, result){
		if(err) throw err;
		console.log(result);
		res.render('index');
	});
});

app.listen(port);
console.log('Server started on port '+port);

module.exports = app;