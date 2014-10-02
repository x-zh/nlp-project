var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
    res.render('index');
});
router.post('/', function(req, res) {
    res.render('index',{
            answer: 'I don\'t have an answer for this.',
            question: req.param('question')
        });
});

module.exports = router;
