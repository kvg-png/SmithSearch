//driver package for sqlite3 used to communicate w database
var sqlite3 = require('sqlite3').verbose()

//db path
const dbPath = "./server/db/courses.db"

//getting copy of class we'll use to start the driver in verbose mode
//verbose mode - it will include full stack trace for any errors (helps w debugging)
let db = new sqlite3.Database(`${dbPath}`, sqlite3.OPEN_READWRITE, (err)=>{
    if (err) return console.error(err.message);
    else console.log('Connected to Course DB ');
});



//exports db for other scripts
module.exports = db