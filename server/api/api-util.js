var mysql = require('mysql');

exports.sqlResponse = function sqlReponse(query, res) {
    // Log it on the screen for debugging
    console.log(query);

    // MySQL Connection Variables
    var connection = mysql.createConnection({
        host: 'dev.spatialdatacapture.org',
        user: 'ucfnmbz',
        password: 'sadohazije',
        database: 'ucfnmbz'
    });

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
