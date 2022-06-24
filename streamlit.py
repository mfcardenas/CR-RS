import streamlit as st
import pandas as pd
import numpy as np
import SessionState
import os
from PIL import Image

import config, rec_sys
from ingredient_parser import ingredient_parser

from word2vec_rec import get_recs

import nltk

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


def make_clickable(name, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = name
    return f'<a target="_blank" href="{link}">{text}</a>'


def main():
    image = Image.open("input/img_wordcloud.png").resize((680, 150))
    st.image(image)
    st.markdown("# *¿Cocinando? :cooking:*")

    st.markdown(
        "POC - Demostrador Nestlé ",
        unsafe_allow_html=True,
    )
    st.markdown(
        "## Dada una lista de ingredientes, ¿qué recetas diferentes puedo hacer? :tomato: "
    )
    st.markdown(
        "Supongamos que desea preparar una receta, ¿qué podría crear? :house: Se propone un modelo que busque en las recetas existentes... :mag: Intente crear la receta! :arrow_down:"
    )

    st.text("")

    session_state = SessionState.get(
        recipe_df="",
        recipes="",
        model_computed=False,
        execute_recsys=False,
        recipe_df_clean="",
    )

    ingredients = st.text_input(
        "Indique los ingredientes a utilizar en la receta (separados con coma)",
        "chirizo, tomate, cebolla, pollo, arroz, etc.",
    )
    session_state.execute_recsys = st.button("¡Recomendar!")

    if session_state.execute_recsys:

        col1, col2, col3 = st.beta_columns([1, 6, 1])
        with col2:
            gif_runner = st.image("input/cooking.gif")
        # recipe = rec_sys.RecSys(ingredients)
        recipe = get_recs(ingredients, mean=True)
        gif_runner.empty()
        session_state.recipe_df_clean = recipe.copy()
        # link is the column with hyperlinks
        recipe["url"] = recipe.apply(
            lambda row: make_clickable(row["recipe"], row["url"]), axis=1
        )
        recipe_display = recipe[["recipe", "url", "ingredients"]]
        session_state.recipe_display = recipe_display.to_html(escape=False)
        session_state.recipes = recipe.recipe.values.tolist()
        session_state.model_computed = True
        session_state.execute_recsys = False

    if session_state.model_computed:
        # st.write("Either pick a particular recipe or see the top 5 recommendations.")
        recipe_all_box = st.selectbox(
            "Estas son las 5 recomendaciones principales, en su defecto, elija una receta en particular.",
            ["Todas!", "Una receta"],
        )
        if recipe_all_box == "Todas!":
            st.write(session_state.recipe_display, unsafe_allow_html=True)
        else:
            selection = st.selectbox(
                "Seleccione una receta especial", options=session_state.recipes
            )
            selection_details = session_state.recipe_df_clean.loc[
                session_state.recipe_df_clean.recipe == selection
            ]
            st.markdown(f"# {selection_details.recipe.values[0]}")
            st.subheader(f"Website: {selection_details.url.values[0]}")
            ingredients_disp = selection_details.ingredients.values[0].split(",")

            st.subheader("Ingredients:")
            col1, col2 = st.beta_columns(2)
            ingredients_disp = [
                ingred
                for ingred in ingredients_disp
                if ingred
                not in [
                    " skin off",
                    " bone out",
                    " from sustainable sources",
                    " minced",
                ]
            ]
            ingredients_disp1 = ingredients_disp[len(ingredients_disp) // 2 :]
            ingredients_disp2 = ingredients_disp[: len(ingredients_disp) // 2]
            for ingred in ingredients_disp1:
                col1.markdown(f"* {ingred}")
            for ingred in ingredients_disp2:
                col2.markdown(f"* {ingred}")
            # st.write(f"Score: {selection_details.score.values[0]}")

    # sidebar stuff
    with st.sidebar.beta_expander("How it works?", expanded=True):
        st.markdown("## How it works? :thought_balloon:")
        st.write(
            "For an in depth overview of the ML methods used and how I created this app, three blog posts are below."
        )
        blog1 = "https://jackmleitch.medium.com/using-beautifulsoup-to-help-make-beautiful-soups-d2670a1d1d52"
        blog2 = "https://towardsdatascience.com/building-a-recipe-recommendation-api-using-scikit-learn-nltk-docker-flask-and-heroku-bfc6c4bdd2d4"
        blog3 = "https://towardsdatascience.com/building-a-recipe-recommendation-system-297c229dda7b"
        st.markdown(
            f"1. [Web Scraping Cooking Data With Beautiful Soup]({blog1})"
        )
        st.markdown(
            f"2. [Building a Recipe Recommendation API using Scikit-Learn, NLTK, Docker, Flask, and Heroku]({blog2})"
        )
        st.markdown(
            f"3. [Building a Recipe Recommendation System Using Word2Vec, Scikit-Learn, and Streamlit]({blog3})"
        )


if __name__ == "__main__":
    main()
