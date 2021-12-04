var express = require('express');
var app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page
app.get('/', function (req, res) {
  res.render('pages/createUser');
});

app.get('/usersList', function (req, res) {
  res.render('pages/usersList');
});

app.get('/createRestraunt', function (req, res) {
  res.render('pages/createRestraunt');
});

app.get('/restrauntsList', function (req, res) {
  res.render('pages/restrauntsList');
});

app.listen(8080);
console.log('Server is listening on port 8080');