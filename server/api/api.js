var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors');

var mysql = require('mysql');

var sqlResponse = require('./api-util.js').sqlResponse;
var crimes = require('./crimes.js');

var api = express();

api.use(bodyParser.json());
api.use(bodyParser.urlencoded());
api.use(cors({
        allowedHeaders: ['X-Requested-With']
}));

api.use(crimes);

api.get('/beats', function(req,res){
        var sql = "SELECT beat_num, wkt, `TOTAL POPULATION` from beat_population";

        sqlResponse(sql, res);
});

api.get('/chicago/wkt', function(req,res){
        sqlResponse("SELECT geometry AS wkt FROM ch_boundaries", res);
});

api.get('/chicago/communities/wkt', function(req, res){
        sqlResponse("SELECT community, geometry AS wkt FROM ch_community", res);
});

module.exports = api;