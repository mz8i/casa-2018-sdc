var express = require('express');
var bodyParser = require('body-parser');

var mysql = require('mysql');

var api = express();

api.use(bodyParser.json());
api.use(bodyParser.urlencoded());


api.get('/crimes', function(req, res, next){
    res.json({dummy: true});
});


module.exports = api;