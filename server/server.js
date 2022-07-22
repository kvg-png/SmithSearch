// import express + create app
var express = require('express')
var app = express()

//driver package for sqlite3 used to communicate w database
var sqlite3 = require('sqlite3').verbose()
var db = require("./db/database.js")


//set up route for api
app.get("/api", (req, res) =>{
    res.json({"users": ["userOne", "userTwo", "userThree"]})
})

app.get("/api/courses", (req, res, next) => {
    var sql = "SELECT title FROM courses"
    var params = []
    db.all(sql, params, (err, rows) => {
        if (err) {
          res.status(400).json({"error":err.message});
          return;
        }
        res.json({
            "message":"success",
            "data":rows
        })
      });
});

app.get("/api/subject", (req, res, next) => {
  var sql = "SELECT subject FROM courses"
  var params = []
  db.all(sql, params, (err, rows) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      res.json({
          "data":rows
      })
    });
});


//Starts backend- port 5000, client on 3000
app.listen(5000, () => {console.log("Server started on port 5000")})