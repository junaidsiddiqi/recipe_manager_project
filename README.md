# Recipe Manager 

## Project Description

A full‑stack web application built with a three‑tier architecture (UI, REST API, Database) that allows users to manage ingredients, create recipes, assign ingredients to recipes, and simulate cooking meals.

---

## Key Features:

Ingredient Management: Add, view, and delete ingredients with live inventory tracking.

Recipe Management: Create new recipes with instructions and view all recipes.

Recipe‑Ingredient Assignment: Link ingredients to recipes with specified amounts.

Cooking Simulation: Cook a recipe, automatically deducting ingredient amounts from inventory.

Error Handling: Prevents cooking if insufficient inventory exists, with clear error messages.

---

## Usage:

Open the project in VSCode for optimal development experience.

**Database:**

-Provision an Amazon RDS MySQL instance.

-Create your schema files (ingredient.sql, recipe.sql, recipeingredient.sql).

-Update creds.py with the RDS endpoint, username, password, and database name.


**Launch the mySQL database**

-Run the mySQL files in the backend folder to establish a connection

*Navigate to the backend directory in VSCode using the command:*

> cd backend


*Install required dependencies for Flask backend:* 

> pip install flask mysql-connector-python

*Start the backend server:*

> python app.py

**Backend runs at: http://localhost:5000**

*Navigate to the frontend directory:*

> cd frontend

*Install required dependencies for Node.js frontend:*
> npm install

*Or install individually:*
> npm install express
> 
> npm install axios
> 
> npm install ejs

*Start the frontend server:*
> node server.js

**Frontend runs at: http://localhost:8080**

---

## Website Screenshots

<img width="1500" height="678" alt="523810816-0ea06b6c-ceb5-4f7f-8580-2f3ffd1594be" src="https://github.com/user-attachments/assets/ef0dfd0b-4774-4b6d-b77e-fd6d66129953" />
<img width="1500" height="696" alt="image" src="https://github.com/user-attachments/assets/6e333c57-796f-43c9-bd55-03a95e91edc6" />
<img width="1500" height="686" alt="image" src="https://github.com/user-attachments/assets/2535a644-0f70-4461-86ce-dcce2a230c4d" />
<img width="1500" height="682" alt="image" src="https://github.com/user-attachments/assets/0a5d3544-e3d6-4e6d-a633-53f5d3486f2e" />
<img width="1500" height="687" alt="image" src="https://github.com/user-attachments/assets/e1fc2767-3e7b-4e30-a6da-8811f89e5422" />

