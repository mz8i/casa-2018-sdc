var express = require('express');
var cors = require('cors');

var mysql = require('mysql');

var sqlResponse = require('./api-util.js').sqlResponse;
var crimes = require('./crimes.js');

var api = express();

api.use(cors({
        allowedHeaders: ['X-Requested-With']
}));

api.use(crimes);

api.get('/beats', function(req,res){
        var sql = "SELECT beat_num as beat_number, wkt, `TOTAL POPULATION` as population from beat_population";

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
        var sql = "SELECT stop_id, stop_lat as lat, stop_lon as lon, beat_num as beat, stop_type as type, stop_name as name FROM (SELECT SYSTEMSTOP, beat_num, 'Bus' as stop_type from bus_beat UNION ALL SELECT STOP_ID, beat_num, 'Rail' as stop_type from rail_beat) stop_beats INNER JOIN stops ON SYSTEMSTOP = stops.stop_id";

        if(req.query.type){
                sql += " WHERE stop_beats.stop_type = " + mysql.escape(req.query.type);
        }
        
        sqlResponse(sql, res);

});

//  API EndPoint to get data from 311 calls aggregated by beat 
api.get('/calls/beats', function (req, res) {

        // SQL Statement to run
        var sql = "SELECT beat_num, Type, count(*) from calls311 group by beat_num, Type" ;

        sqlResponse(sql, res);
   
});

//  API EndPoint to get data from transport stops aggregated by Beat
api.get('/stops/beats', function (req, res) {
        // SQL Statement to run
        var sql = "SELECT beat_num, stop_type, count(SYSTEMSTOP) FROM (SELECT SYSTEMSTOP, beat_num, 'Bus' as stop_type from bus_beat UNION ALL SELECT STOP_ID, beat_num, 'Rail' as stop_type from rail_beat) agg_beats GROUP BY beat_num, stop_type";

        sqlResponse(sql, res);

});

//  API EndPoint to get data from transport routes
api.get('/chicago/transit/wkt', function (req, res) {
        var sql = "SELECT rs.geometry, rt.route_type_name FROM route_shapes rs JOIN trips t ON rs.shape_id = t.shape_id JOIN routes r ON t.route_id = r.route_id JOIN route_type rt ON r.route_type = rt.route_type", res;
        
        sqlResponse(sql, res);
});
        if(req.query.type){
                sql += " WHERE route_type_name = " + mysql.escape(req.query.type);
        }



module.exports = api;