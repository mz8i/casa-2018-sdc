var express = require('express');
var http = require('http');
var path = require('path');
var engines = require('consolidate');

var config = require('./config.js');
var api = require('./api/api.js');

var app = express();

app.engine('.html', engines.ejs);
app.set('view engine', '.html');
app.set('views', path.join(__dirname, 'public') );

app.use(express.urlencoded());

app.use('/static', express.static('public'));

app.use('/api', api);

app.get('/', function(req, res){
    res.render('index.html');
});

app.listen(config.port);
