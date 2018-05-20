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


//  API EndPoint to get data from 311 calls 
api.get('/calls', function (req, res) {

        // If all the variables are provided connect to the database
        if (req.query.beat) {

                // Parse the values from the URL into numbers for the query
                var beat = req.query.beat;

                // SQL Statement to run
                var sql = "SELECT calls311.Lat, calls311.Lon, calls311.RealCreationDate, calls311.RespTime FROM calls311 WHERE beat_num=" + mysql.escape(beat) ;
                if (beat) sql += " and beat_num = " + mysql.escape(type);

                sqlResponse(sql, res);
        } else {
                // If all the URL variables are not passed send an empty string to the user
                res.send("");
        }
});


//  API EndPoint to get data from transport stops 
api.get('/stops', function (req, res) {
        // SQL Statement to run
        var sql = "SELECT SYSTEMSTOP, stop_id, stop_lat, stop_lon, beat_num, stop_type, stop_name FROM (SELECT SYSTEMSTOP, beat_num, 'Bus' as stop_type from bus_beat UNION ALL SELECT STOP_ID, beat_num, 'Rail' as stop_type from rail_beat) stop_beats INNER JOIN stops ON SYSTEMSTOP = stops.stop_id";
        
        sqlResponse(sql, res);

});

//  API EndPoint to get data from 311 calls aggregated by beat 
api.get('/calls/beats', function (req, res) {

        // SQL Statement to run
        var sql = "SELECT beat_num, Type from calls311 group by beat_num, Type" ;

        sqlResponse(sql, res);
   
});

//  API EndPoint to get data from transport stops aggregated by Beat
api.get('/stops/beats', function (req, res) {
        // SQL Statement to run
        var sql = "SELECT beat_num, stop_type, count(SYSTEMSTOP) FROM (SELECT SYSTEMSTOP, beat_num, 'Bus' as stop_type from bus_beat UNION ALL SELECT STOP_ID, beat_num, 'Rail' as stop_type from rail_beat) agg_beats GROUP BY beat_num, stop_type";

        sqlResponse(sql, res);

});



module.exports = api;