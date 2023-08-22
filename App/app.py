import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import ImageTk, Image
import requests
import io
import webbrowser
import ast
import pandas as pd

class RecipeRecommendationApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Recommendation Application")
        
        # Load the DataFrame
        self.clean_data()

        # Set window size (width x height)
        self.root.geometry("1100x700")  # Replace with desired dimensions

        # Set background color of the window
        self.root.configure(bg="#DCDCDC")  # Replace with desired color

        self.create_widgets()
        
    def clean_data(self):
        self.data = pd.read_csv('data/Recipes2.csv')
        self.data = self.data[self.data['duration'].notnull()]
        self.data['duration'] = self.data['duration'].astype(int)
        self.data['difficulty'] = self.data['difficulty'].str.lower()
        self.data.reset_index(inplace=True)
        self.data['cleaned_ingredients'] = self.data['cleaned_ingredients'].apply(ast.literal_eval)
        self.data = self.data.drop(columns=["index", "ingredients", "ingredients_processed", "removed_stopwords"])
    
    def create_widgets(self):
        self.ingredients_label = tk.Label(
            self.root, text="Ingredients (comma-separated):",
            fg="#000080")  # Dark Blue
        self.ingredients_entry = tk.Entry(self.root)
        self.duration_label = tk.Label(
            self.root,
            text="Max Preparation Duration (minutes):",
            fg="#000080")  # Dark Blue
        self.duration_slider = tk.Scale(self.root,
                                        from_=5,
                                        to=55,
                                        orient="horizontal",
                                        fg="#000080")  # Dark Blue
        self.difficulty_label = tk.Label(self.root,
                                         text="Preparation Difficulty:",
                                         fg="#000080")  # Dark Blue
        self.difficulty_var = tk.StringVar()
        self.difficulty_dropdown = tk.OptionMenu(self.root,
                                                 self.difficulty_var,
                                                 "very easy", "easy",
                                                 "moderate", "hard",
                                                 "very hard")
        self.recommend_button = tk.Button(self.root,
                                          text="Recommend Recipes",
                                          command=self.recommend_recipes,
                                          fg="#000080")  # Dark Blue

        # Pack widgets
        self.ingredients_label.pack()
        self.ingredients_entry.pack()
        self.duration_label.pack()
        self.duration_slider.pack()
        self.difficulty_label.pack()
        self.difficulty_dropdown.pack()
        self.recommend_button.pack()

        # Create a frame to display results (initially empty)
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack()

    def recommend_recipes(self):
        # Extract user input and preferences
        ingredients = self.ingredients_entry.get().split(',')
        max_duration = self.duration_slider.get()
        desired_difficulty = self.difficulty_var.get().lower()

        # Instantiate and fit the TfidfVectorizer
        vectorizer = TfidfVectorizer()
        ingredients_matrix = vectorizer.fit_transform([
            ' '.join(ingredients)
            for ingredients in self.data['cleaned_ingredients']
        ])

        # User-provided ingredients
        user_ingredients_vector = vectorizer.transform([' '.join(ingredients)])

        # Calculate cosine similarity
        similarities = cosine_similarity(user_ingredients_vector,
                                         ingredients_matrix).flatten()

        filtered_recipes = []
        for idx, recipe in enumerate(self.data['name']):
            if self.data['duration'][idx] <= max_duration and self.data['difficulty'][
                    idx] == desired_difficulty:
                filtered_recipes.append((recipe, similarities[idx]))

        filtered_recipes.sort(key=lambda x: x[1], reverse=True)
        
        # Display results in the results frame
        self.results_frame.destroy()
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack()

        # Display results in the results frame
        for idx, (recipe, similarity) in enumerate(filtered_recipes[:3]):
            if similarity > 0:
                URL = self.data[self.data['name'] == recipe]['URL'].values[0]
                url = self.data[self.data['name'] == recipe]['img_url'].values[0]
                img_data = requests.get(url).content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((150, 150), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)

                recipe_text = f"{idx+1}. {recipe} (Similarity : {similarity:.2f})"
                recipe_label = tk.Label(
                    self.results_frame,
                    text=recipe_text,
                    fg="#0000FF",  # Blue color for hyperlink appearance
                    cursor="hand2"  # Change cursor to hand on hover
                )
                recipe_label.pack()

                # Bind the callback to the label (outside the loop)
                recipe_label.bind("<Button-1>", lambda event, url=URL: self.open_url(event, url))

                # Display recipe image
                img_label = tk.Label(self.results_frame, image=img)
                img_label.image = img
                img_label.pack()
            else:
                # Display message when no matching recipes
                no_recipe_label = tk.Label(
                    self.results_frame, text="No recipes match your criteria.")
                no_recipe_label.pack()

    def open_url(self, event, url):
        webbrowser.open(url)  # Open URL in default web browser

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeRecommendationApp(root)
    root.mainloop()
