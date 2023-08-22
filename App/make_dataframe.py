import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from utils import PercentBar
import threading
from tqdm import tqdm

class MakeDataFrame:

    def __init__(self):
        self.utils = PercentBar()
        self.full_recipe_links = []
        self.loading_bar_interrupted = False
        self.foods = [
            # Meats and Fish
            "chicken",
            "beef",
            "pork",
            "lamb",
            "veal",
            "turkey",
            "duck",
            "fish",
            "salmon",
            "tuna",
            "shrimp",
            "mussels",
            "oysters",
            "bacon",
            "ham",

            # Vegetables
            "carrot",
            "potato",
            "tomato",
            "onion",
            "garlic",
            "spinach",
            "broccoli",
            "zucchini",
            "eggplant",
            "bell pepper",
            "mushroom",
            "green beans",
            "asparagus",
            "cabbage",
            "celery",
            "cucumber"

            # Fruits
            "apple",
            "banana",
            "orange",
            "strawberries",
            "grapes",
            "pear",
            "pineapple",
            "kiwi",
            "melon",
            "mango",
            "avocado",
            "cherry",
            "raspberry",
            "blueberry",
            "lime",
            "lemon",
            "coconut"

            # Dairy Products
            "milk",
            "cheese",
            "butter",
            "yogurt",
            "cream",
            "ice cream",

            # Grains
            "rice",
            "pasta",
            "bread",
            "flour",
            "oats",
            "barley",
            "quinoa",

            # Legumes
            "red beans",
            "lentils",
            "chickpeas",
            "fava beans",

            # Herbs and Spices
            "basil",
            "parsley",
            "thyme",
            "rosemary",
            "oregano",
            "cumin",
            "coriander",
            "cinnamon",
            "turmeric",
            "paprika",
            "pepper",
            "salt",

            # Condiments and Sauces
            "ketchup",
            "mustard",
            "mayonnaise",
            "balsamic vinegar",
            "soy sauce",
            "tomato sauce",
            "barbecue sauce",
            "hot sauce",
            "olive oil",
            "vinaigrette",
            "mint"

            # Nuts and Seeds
            "almonds",
            "cashews",
            "walnuts",
            "pistachios",
            "sunflower seeds",
            "sesame seeds",
            "chia seeds",

            # Sweeteners
            "sugar",
            "honey",
            "maple syrup",
            "stevia",
            "syrup",
            "chocolate"

            # Beverages
            "water",
            "coffee",
            "fruit juice",
            "almond milk",
            "coconut milk",

            # Others
            "eggs",
            "egg",
            "almond flour",
            "coconut flour",
            "yeast",
            "sourdough starter"
        ]

        self.stop_words = set(stopwords.words('english'))

    def scrape_recipes_page(self, page_number):
        base_url = "https://recipes.lewagon.com/"
        params = {"page": page_number}

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        else:
            print(f"Error while retrieving page {page_number}.")
            return None

    def extract_preparation_duration(self, description_text):
        duration_pattern = r"(\d+)\s*minutes"
        duration_match = re.search(duration_pattern, description_text)
        if duration_match:
            preparation_duration = duration_match.group(1)
            return preparation_duration
        return None

    def scrape_recipe_info(self, recipe_url):
        response = requests.get(recipe_url)

        if response.status_code == 200:
            recipe_soup = BeautifulSoup(response.content, "html.parser")

            name = recipe_soup.find("h2").text.strip()

            img_element = recipe_soup.find("img",
                                           class_="recipe-img mb-3 mb-md-0")
            img_url = img_element['src'] if img_element else ''

            ingredient_spans = recipe_soup.find_all("p", class_="mb-0")
            ingredients = [span.text.strip() for span in ingredient_spans]

            description_element = recipe_soup.find(
                "p", class_="text-justify recipe-description")
            description_text = description_element.get_text(
            ) if description_element else ""
            duration = self.extract_preparation_duration(description_text)

            difficulty_element = recipe_soup.find("span",
                                                  class_="recipe-difficulty")
            difficulty = difficulty_element.text.strip(
            ) if difficulty_element else ""

            return {
                "name": name,
                "ingredients": ingredients,
                "duration": duration,
                "difficulty": difficulty,
                "img_url": img_url
            }
        else:
            print(f"Error while retrieving recipe {recipe_url}.")
            return None

    def clean_ingredients(self, ingredient):
        cleaned_ingredient = re.sub(r"\d+|/", "", ingredient).strip()
        return cleaned_ingredient
    

    def preprocess_ingredients(self, ingredient_list):
        processed_ingredients = []
        removed_stopwords = []
        for ingredient in ingredient_list:
            ingredient_lower = ingredient.lower().replace(',',
                                                          '').replace('.', '')
            if ingredient_lower not in self.stop_words:
                processed_ingredients.append(ingredient_lower)
            else:
                removed_stopwords.append(ingredient_lower)
        return processed_ingredients, removed_stopwords

    def real_ingredients(self, ingredients):
        cleaned_ingredients = []
        for ingredient in ingredients:
            ingredient = re.sub(r'(\w+)\)', r'\1', ingredient)
            words = ingredient.split()
            new_words = [
                word for word in words
                if any(food in word for food in self.foods)
            ]
            cleaned_ingredient = ', '.join(new_words)
            
             # Remove any quotation marks present
            cleaned_ingredient = cleaned_ingredient.replace('"', '').replace("'", '')
        
            if cleaned_ingredient:
                cleaned_ingredients.append(cleaned_ingredient)
        return cleaned_ingredients


    def make_dataframe_with_loading_bar(self, total_pages):
        min_recipes_per_page = 4
        max_recipes_per_page = 13
        data = None 
    
        def make_dataframe_task(progress_callback):
            nonlocal data

            # Step 1: Scrape full recipe links
            for page_number in tqdm(range(1, total_pages + 1), desc="Scraping pages"):
                list_soup = self.scrape_recipes_page(page_number)

                if list_soup:
                    recipe_articles = list_soup.find_all("div",
                                                        class_="recipe my-3")
                    num_recipes_on_page = min(
                        max_recipes_per_page,
                        max(min_recipes_per_page, len(recipe_articles)))

                    for i in range(num_recipes_on_page):
                        recipe_link = recipe_articles[i]["data-href"]
                        full_recipe_link = recipe_link
                        self.full_recipe_links.append(full_recipe_link)
                else:
                    print(
                        f"Unable to retrieve the list of recipes for page {page_number}."
                    )

            # Step 2: Scrape individual recipes and store data in recipes_data
            recipes_data = []

            for full_recipe_link in tqdm(self.full_recipe_links, desc="Scraping recipes"):
                if not self.loading_bar_interrupted:
                    recipe_info = self.scrape_recipe_info(full_recipe_link)
                    if recipe_info:
                        recipes_data.append(recipe_info)
                    else:
                        break

            if not self.loading_bar_interrupted:
                data = pd.DataFrame(recipes_data)

                # Step 3: Preprocess ingredients
                data['ingredients'] = data['ingredients'].apply(
                lambda ingredients:
                [self.clean_ingredients(ingredient) for ingredient in ingredients])

                data['ingredients_processed'], data['removed_stopwords'] = zip(
                *data['ingredients'].apply(self.preprocess_ingredients))

                # Step 4: Apply real_ingredients function
                data['cleaned_ingredients'] = data['ingredients_processed'].apply(self.real_ingredients)

                # Step 5: Save to CSV
                data.to_csv('data/Recipes.csv', index=False)
            else:
                data = None
                
            return data
            
            
        def update_loading_bar_task(percentage):
            percentage = 0
            while not self.loading_bar_interrupted and percentage < 100:
                self.update_loading_bar(percentage)
                percentage += 1
                time.sleep(0.1)  # Adjust the interval as needed

        loading_thread = threading.Thread(target=update_loading_bar_task, args=(0,))
        processing_thread = threading.Thread(target=make_dataframe_task, args=(loading_thread,))
    
        loading_thread.start()
        processing_thread.start()

        self.loading_bar_interrupted = False

        processing_thread.join()

        print()  # Print a newline to clear the loading bar

        if data is not None:
            print("DataFrame updated")
        else:
            print("DataFrame update interrupted")
        
        time.sleep(1)

if __name__ == "__main__":
    NB_PAGES = 123
    make_dataframe_instance = MakeDataFrame()
    make_dataframe_instance.make_dataframe_with_loading_bar(NB_PAGES)