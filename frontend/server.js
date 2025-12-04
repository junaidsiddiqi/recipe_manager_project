var express = require('express');
var axios = require('axios');
var app = express();

app.set('view engine', 'ejs');

// Home page
app.get('/', function(req, res) {
    res.render('index');
});

// Show ingredients
app.get('/ingredients', function(req, res) {
    axios.get('http://localhost:5000/api/ingredient/all')
        .then(function(response) {
            res.render('ingredients', { ingredients: response.data });
        })
        .catch(function() {
            res.render('ingredients', { ingredients: [] });
        });
});

// Show recipes
app.get('/recipes', function(req, res) {
    axios.get('http://localhost:5000/api/recipe/all')
        .then(function(response) {
            res.render('recipes', { recipes: response.data });
        })
        .catch(function() {
            res.render('recipes', { recipes: [] });
        });
});

// Cook a recipe (view)
app.get('/cook/:id', function(req, res) {
    var recipeId = req.params.id;
    axios.get('http://localhost:5000/api/recipe?id=' + recipeId)
        .then(function(response) {
            res.render('cook', { recipe: response.data, recipeId: recipeId });
        })
        .catch(function() {
            res.render('cook', { recipe: [], recipeId: recipeId });
        });
});

// Cook a recipe 
app.post('/cook/:id', function(req, res) {
    var recipeId = req.params.id;
    axios.post('http://localhost:5000/api/recipe/cook', { recipeid: recipeId })
        .then(function(response) {
            res.send(response.data);
        })
        .catch(function() {
            res.send("Error cooking recipe");
        });
});

app.listen(8080, function() {
    console.log('8080 is the magic port');
});
