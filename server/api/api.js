var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors');

var mysql = require('mysql');

var api = express();

api.use(bodyParser.json());
api.use(bodyParser.urlencoded());
api.use(cors({
        allowedHeaders: ['X-Requested-With']
}));

// MySQL Connection Variables
var connection = mysql.createConnection({
  host     : 'dev.spatialdatacapture.org',
  user     : 'ucfnmbz',
  password : 'sadohazije',
  database : 'ucfnmbz'
});

function sqlResponse(query, res) {
        // Log it on the screen for debugging
        console.log(query);

        // Run the SQL Query
        connection.query(query, function (err, rows, fields) {
                if (err) console.log("Err:" + err);
                if (rows != undefined) {
                        // If we have data that comes bag send it to the user.
                        res.send(rows);
                } else {
                        res.send("[]");
                }
        });
}


api.get('/crimes', function(req, res, next){
    res.json({dummy: true});
});


api.get('/crimes/types', function(req, res){
        var sql = "SELECT DISTINCT PrimaryType FROM Crimes";

        sqlResponse(sql, res);
});

//  API EndPoint to get data from a specific type and year
api.get('/crimes/:year/:primarytype', function (req, res) {

      // If all the variables are provided connect to the database
      if(req.params.primarytype != "" && req.params.year){
               
                // Parse the values from the URL into numbers for the query
                var year = parseFloat(req.params.year);
                var primarytype = req.params.primarytype;

                // SQL Statement to run
              var sql = "SELECT Crimes.Beat, Crimes.District, Crimes.Ward, Crimes.Latitude, Crimes.Longitude, Crimes.Date FROM Crimes WHERE PrimaryType = "+connection.escape(primarytype)+" and YEAR = "+year+"";
              
              sqlResponse(sql, res);
        }else{
                // If all the URL variables are not passed send an empty string to the user
                res.send("");
        }
});


//  API EndPoint to get data from a specific type and year, for heatmap draw
api.get('/crimes/:year/:primarytype/coordinates', function (req, res) {

        // If all the variables are provided connect to the database
        if (req.params.primarytype != "" && req.params.year) {

                // Parse the values from the URL into numbers for the query
                var year = parseFloat(req.params.year);
                var primarytype = req.params.primarytype;

                // SQL Statement to run
                var sql = "SELECT Crimes.Latitude, Crimes.Longitude FROM Crimes WHERE PrimaryType = " + connection.escape(primarytype) + " and YEAR = " + year + "";

                sqlResponse(sql, res);
        } else {
                // If all the URL variables are not passed send an empty string to the user
                res.send("");
        }
});


//  API EndPoint to get data for all year , of a specific crime typr
api.get('/crimes/:primarytype', function (req, res) {

        // If all the variables are provided connect to the database
        if (req.params.primarytype != "" && req.params.year) {

                // Parse the values from the URL into numbers for the query
                
                var primarytype = req.params.primarytype;

                // SQL Statement to run
                var sql = "SELECT Crimes.Date, Crimes.Latitude, Crimes.Longitude, Crimes.Date FROM Crimes WHERE PrimaryType = " + connection.escape(primarytype) + " ";

               sqlResponse(sql, res);
        } else {
                // If all the URL variables are not passed send an empty string to the user
                res.send("");
        }
});


module.exports = api;