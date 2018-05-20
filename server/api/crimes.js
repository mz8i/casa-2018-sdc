var express = require('express');
var hexbin = require('d3-hexbin');

var sqlResponse = require('./api-util.js').sqlResponse;

var api = express();

api.get('/crimes/types', function (req, res) {
    var sql = "SELECT FBIType as code, Description as type FROM FBICrimeTypes";

    sqlResponse(sql, res);
});

//  API EndPoint to get data from a specific type and year
api.get('/crimes', function (req, res) {

    // If all the variables are provided connect to the database
    if (req.query.type && req.query.year) {
        // Parse the values from the URL into numbers for the query
        var year = parseInt(req.query.year);
        var type = req.query.type;

        // SQL Statement to run
        var sql = "SELECT Crimes.Beat, Crimes.District, Crimes.Ward, Crimes.Latitude, Crimes.Longitude, Crimes.Date FROM Crimes WHERE FBICode = " + mysql.escape(type) + " and YEAR = " + year + "";

        sqlResponse(sql, res);
    } else {
        // If all the URL variables are not passed send an empty string to the user
        res.send("");
    }
});


//  API EndPoint to get data from a specific type and year, for heatmap draw
api.get('/crimes/coordinates', function (req, res) {

    // If all the variables are provided connect to the database
    if (req.query.year) {

        // Parse the values from the URL into numbers for the query
        var year = parseInt(req.query.year);
        var type = req.query.type;

        // SQL Statement to run
        var sql = "SELECT Crimes.Latitude, Crimes.Longitude FROM Crimes WHERE Year = " + year;
        if (type) sql += " and FBICode = " + mysql.escape(type);

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
        var sql = "SELECT Crimes.Date, Crimes.Latitude, Crimes.Longitude, Crimes.Date FROM Crimes WHERE PrimaryType = " + mysql.escape(primarytype) + " ";

        sqlResponse(sql, res);
    } else {
        // If all the URL variables are not passed send an empty string to the user
        res.send("");
    }
});

module.exports = api;