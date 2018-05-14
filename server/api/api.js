var express = require('express');
var bodyParser = require('body-parser');

var mysql = require('mysql');

var api = express();

api.use(bodyParser.json());
api.use(bodyParser.urlencoded());

// MySQL Connection Variables
var connection = mysql.createConnection({
  host     : 'dev.spatialdatacapture.org',
  user     : 'ucfnmbz',
  password : 'sadohazije',
  database : ''
});


api.get('/crimes', function(req, res, next){
    res.json({dummy: true});
});



//  API EndPoint to get data from a specific type and year
app.get('/crimes/:year/:primarytype', function (req, res) {

      // Alows data to be downloaded from the server with security concerns
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Headers", "X-Requested-WithD");
      // If all the variables are provided connect to the database
      if(req.params.primarytype != "" && req.params.year){
               
                // Parse the values from the URL into numbers for the query
                var year = parseFloat(req.params.year);

                // SQL Statement to run
                var sql = "SELECT Crimes.Beat, Crimes.District, Crimes.Ward, Crimes.Latitude, Crimes.Longitude Crimes.Hour, Crimes.Tesdate FROM Crimes WHERE PRIMARY TYPE = "+primarytype+" and YEAR == "+year+"";
                
                // Log it on the screen for debugging
                console.log(sql);

                // Run the SQL Query
                connection.query(sql, function(err, rows, fields) {
                        if (err) console.log("Err:" + err);
                        if(rows != undefined){
                                // If we have data that comes bag send it to the user.
                                res.send(rows);
                        }else{
                                res.send("");
                        }
                });
        }else{
                // If all the URL variables are not passed send an empty string to the user
                res.send("");
        }
});








module.exports = api;