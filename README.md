# A simple Finance Tracker and Dashboard web app using Flask, Dash, and SQLite.

## Table of contents:
<a id="table-of-contents"></a>

1. [About the project](#heading-1)
2. [Standard and external packages used for this project](#heading-2)
3. [Other technologies used for this project](#heading-3)
4. [Project structure](#heading-4)

<a id="heading-1"></a>

## [About the project](#table-of-contents)

This project serves as an example of how I learned how to use Flask and Dash (from Plotly) to create a simple web application. The user enters their income and expense history, and the app saves that data to a built-in SQLite database. Then, with the data that it has, it will generate a dashboard using Dash.

For the project structure, I followed this [tutorial](https://hackersandslackers.com/flask-application-factory/) so that I would learn to create a Flask app that is scalable. This will help me adapt easily to a project that has a lot of required functionalities in the future. Finally, for the Dash app, I also followed this [tutorial](https://hackersandslackers.com/plotly-dash-with-flask/), which is also from the same website and author. The Dash app is also created to be scalable. With this tutorial, I learned how to set the Flask app as the server and load the Dash app on it to retain the functionalities of the Flask app.

<a id="heading-2"></a>

### [Standard and external packages used for this project:](#table-of-contents)

* **Flask** - This is the web framework that I used for this project.
* **Flask-SQLAlchemy** - A package that simplifies the process of using SQLAlchemy in my Flask app. Used for CRUD applications via ORM.
* **SQLite3** - I used this for some functions for which I am more comfortable using traditional SQL queries.
* **Dash** - I used this to display the plots that I created using Plotly.
* **Plotly** - This is used to configure and generate plots. 
* **Pandas** - I used this to load data from the database and apply some data manipulation so that the data is easier to use when making computations and data visualizations.

<a id="heading-3"></a>

### [Other technologies used for this project:](#table-of-contents)

* **HTML** - This is used for defining how the data will be structured - Headers, Footers, Tables, Forms, Div, etc.
* **CSS** - The visual settings for the HTML.
* **JavaScript** - Used for functions that deals with form submissions.
* **JQuery** - This is only used once for showing and hiding the rest of the form for adding a transaction (income or expense).
* **jinja2** - This is used to dynamically display data from the Flask app.

<a id="heading-4"></a>

## [Project Structure](#table-of-contents)
```
├── README.md                                   <- This README. Top level README.
│
├── .gitignore                                  <- Lists all the things that should not be uploaded to this GitHub repository.
│
├── config.py                                   <- Contains the configuration settings for the app.
│
├── environment.yml                             <- A .yml file that can be use to create a conda env.
│
├── main.py                                     <- Main .py file. Runs the whole app.
│
├── requirements.txt                            <- Alternative to .yml file when the user want an venv instead of conda env.
│
├── backups\output_files                        <- This is where the generated .csv files are saved when the user creates a backup for the SQL database. This is also used to restore the database.
│
└── application                                 <- Contains all of the files neccessary for the app.
    ├── dashboard                               <- Contains the .py files needed by the Dash app.
    │   ├── __init__.py                         <- init file for the Dash app. 
    │   │
    │   ├── callbacks.py                        <- callbacks for the Dash app.
    │   │
    │   ├── functions.py                        <- Contains several functions needed for the Dash app. Mostly managing dataframes using Pandas.
    │   │
    │   └── layout.py                           <- app.layout of the Dash app.
    │
    ├── static                                  <- Static folder.
    │   ├── assets                              <- Contains the visuals needed for the project such as images.
    │   │
    │   ├── css                                 <- css Folder.
    │   │   └── styles.css                      <- Universal style.css for the whole project.
    │   │
    │   ├── db                                  <- Database folder.
    │   │   └── finance.db                      <- The database.
    │   │
    │   └── schema                              <- Contains the query needed for some of the functions for the app.
    │       ├── backup_table_creation.sql       <- Creates (if not exists) a table for the backups.
    │       │
    │       └── finance__table_creation.sql     <- Creates (if not exists) a table and is solely used for restoring the database using the selected .csv file.
    │   
    ├── templates                               <- Contains the .html files which loads the data dynamically using jinja2 expressions.
    │   ├── about_me.html                       <- Contains details about me. My Resume.
    │   │
    │   ├── base.html                           <- Contains the base format of the page. Other .html files inherits this using jinja2 expression.
    │   │
    │   ├── file_selection.html                 <- Loads the list of backup files to be selected to use to restore the database.
    │   │
    │   ├── index.html                          <- index or homepage of the app. Loads the overall data and the CRUD functionality of the app.
    │   │
    │   └── update.html                         <- Loads the update form for the selected data.
    │
    ├── __init__.py                             <- init file for the Flask app.
    │
    ├── models.py                               <- Models or the table creation.
    │
    ├── routes.py                               <- Contains the routes for the Flask app.
    │
    └── utilities.py                            <- Contains several functions needed for the Flask app.
```

## Thank you for visiting!