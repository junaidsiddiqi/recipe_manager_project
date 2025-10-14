"ingredient table"
CREATE TABLE ingredient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ingredientname VARCHAR(100) NOT NULL,
    totalamount INT NOT NULL
);

"recipe table"
CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instructions TEXT NOT NULL
);

"recipeingredient table"
CREATE TABLE recipeingredient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipeid INT NOT NULL,
    ingredientid INT NOT NULL,
    amount INT NOT NULL,
    FOREIGN KEY (recipeid) REFERENCES recipe(id),
    FOREIGN KEY (ingredientid) REFERENCES ingredient(id)
);

