var immunio = require('immunio');
const express = require('express');
const app = express();
const port = 80;

var multer  = require('multer');
var upload = multer({ dest: 'uploads/' });

app.get('/', (req, res) => res.send('Hello World!'));

app.post('/upload', upload.single('file'), function (req, res, next) {
  const file = req.file;
  if (!file) {
    const error = new Error('Please upload a file');
    error.httpStatusCode = 400;
    return next(error);
  }
  res.send(file);
});


app.listen(port, () => console.log(`Example app listening on port ${port}!`));