# <center><u><b>Recipe App</b></u></center>

<center>
<img src="recipe.png" alt="Description de l'image">
</center>

This is a recipe application that scrapes recipes from a fictional cooking website, processes the data, and provides a user interface for searching and exploring recipes.

## Contents

- **Overview**
- **The App**
- **Project Structure**
- **Getting Started**
- **Notebooks**
- **Dependencies**
- **Credit and Contribution**

## Overview

The Recipe App is designed to scrape recipes, process the data, and present it in a user-friendly way. It consists of several components including a scraper, data processing, a user interface, and notebooks for exploration.


## The App

<center>
<img src="appli.png" alt="app">
</center>

## Project Structure

- App/  
    - app.py: Main application file containing user interface functionality.
    - make_dataframe.py: Module for scraping and processing recipes to a dataframe.
    - utils.py: Utility functions used throughout the project.
- data/  
    - Recipes.csv: Processed data containing recipes.  
- notebook/
    - scraping.ipynb: Notebook exploring web scraping.
    - class_creation.ipynb: Notebook for creating classes.
    - app_creation.ipynb: Notebook for creating the application.    
- Makefile: Makefile for running scripts.  
- requirements.txt: List of project dependencies.  


## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/CassienBABEY/What-do-I-cook-Tonight.git
2. Install project dependencies:
    ```bash
    pip install -r requirements.txt
3. Run the scripts using the Makefile:
    ```bash
    make update-data NB_PAGES={insert number}  # Run the scraper to collect recipe data from the website into a dataframe

    make run-app # Explore recipes using the Recipe App's user interface
    ```

## Notebooks

The notebook/ directory contains Jupyter notebooks used for exploration and development. These notebooks were used to refine the scraping process, create classes, and build the application.


## Dependencies

The following Python packages are required for running the project:

- `beautifulsoup4`
- `nltk`
- `pandas`
- `Pillow`
- `requests`
- `scikit-learn`
- `tqdm`


You can install these dependencies using the provided requirements.txt file:
```bash
pip install -r requirements.txt
```

## Credit and Contributions

This project was developed by <b>Cassien BABEY</b>.

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

For more information about the dataset, please send me a message or add a comment.
