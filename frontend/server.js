var express = require('express');
var axios = require('axios');
var app = express();

// Setting up ejs as the view engine
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const API = "http://localhost:5000/api";

// Homepage
app.get('/', function(req, res) {
    res.render('index');
});

// Show all ingrdients
app.get('/ingredients', function(req, res) {
    axios.get(API + '/ingredient/all')
        .then(function(response) {
            res.render('ingredients', { ingredients: response.data, message: null });
        })
        .catch(function() {
            res.render('ingredients', { ingredients: [], message: "Error fetching ingredients" });
        });
});

// Add ingredient
app.post('/ingredients/add', function(req, res) {
    var name = req.body.name;
    var amount = parseInt(req.body.amount, 10);

    axios.post(API + '/ingredient', { ingredientname: name, totalamount: amount })
        .then(function() {
            res.redirect('/ingredients');
        })
        .catch(function() {
            res.send("Error adding ingredient");
        });
});

// Delete ingredient
app.post('/ingredients/delete', function(req, res) {
    var id = req.body.id;

    axios.delete(API + '/ingredient', { data: { id } })
        .then(function() {
            res.redirect('/ingredients');
        })
        .catch(function() {
            res.send("Error deleting ingredient");
        });
});

// Show all recipes
app.get('/recipes', function(req, res) {
    axios.get(API + '/recipe/all')
        .then(function(response) {
            res.render('recipes', { recipes: response.data, message: null });
        })
        .catch(function() {
            res.render('recipes', { recipes: [], message: "Error fetching recipes" });
        });
});

// Add recipe
app.post('/recipes/add', function(req, res) {
    var name = req.body.name;
    var instructions = req.body.instructions;

    axios.post(API + '/recipe', { name, instructions })
        .then(function() {
            res.redirect('/recipes');
        })
        .catch(function() {
            res.send("Error adding recipe");
        });
});


// Show recipes and ingredients assigned
app.get('/recipeingredient', function(req, res) {
    axios.all([
        axios.get(API + '/recipe/all'),
        axios.get(API + '/ingredient/all')
    ])
    .then(axios.spread(function(recipesRes, ingredientsRes) {
        res.render('recipeingredient', { 
            recipes: recipesRes.data, 
            ingredients: ingredientsRes.data,
            message: null
        });
}))
    .catch(function() {
        res.render('recipeingredient', 
            { recipes: [], 
            ingredients: [], 
            message: "Error loading data" });
        });
});

// Assign ingredient to recipe
app.post('/recipeingredient', function(req, res) {
    var recipeid = req.body.recipeid;
    var ingredientid = req.body.ingredientid;
    var amount = req.body.amount;

    axios.post(API + '/recipeingredient', { recipeid, ingredientid, amount })
        .then(function() {
            res.redirect('/recipeingredient');
        })
        .catch(function() {
            res.send("Error assigning ingredient to recipe");
        });
});

// Show recipe selection 
app.get('/cook', function(req, res) {
    axios.get(API + '/recipe/all')
        .then(function(response) {
            res.render('cook_select', 
                { recipes: response.data, 
                recipe: [], 
                recipeId: null, 
                message: null });
        })
        .catch(function() {
            res.render('cook_select', 
                { recipes: [], 
                recipe: [], 
                recipeId: null, 
                message: "Error loading recipes" });
        });
});

// Select the recipe to cook
app.post('/cook/select', function(req, res) {
    var recipeId = req.body.recipeid;

    axios.get(API + '/recipe?id=' + recipeId)
        .then(function(response) {
            axios.get(API + '/recipe/all')
                .then(function(allRecipes) {
                    res.render('cook_select', { 
                        recipes: allRecipes.data, 
                        recipe: response.data, 
                        recipeId: recipeId, 
                        message: null 
                    });
                });
        })
        .catch(function() {
            res.render('cook_select', 
                { recipes: [], 
                recipe: [], 
                recipeId: recipeId, 
                message: "Error loading recipe" });
        });
});

// Cook the recipe
app.post('/cook/:id', function(req, res) {
    var recipeId = req.params.id;

    axios.post(API + '/recipe/cook', { recipeid: recipeId })
        .then(function(response) {
            axios.get(API + '/recipe?id=' + recipeId)
                .then(function(recipeRes) {
                    res.render('cook_select', {
                        recipes: recipeRes.data,
                        recipe: recipeRes.data,
                        recipeId: recipeId,
                        message: response.data
                    });
                });
        })
        .catch(function() {
            res.render('cook_select', {
                recipes: [],
                recipe: [],
                recipeId: recipeId,
                message: "Error cooking recipe"
            });
        });
});

app.listen(8080, function() {
    console.log('8080 is the magic port');
});
