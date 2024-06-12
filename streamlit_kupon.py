import streamlit as st
import pandas as pd
import numpy as np
import io

st.title("Tipskupon")

df = pd.read_csv('Webapp/fixtures.csv')
df_res = pd.read_csv('Webapp/results.csv')

result_choices = ["1", "X", "2"]
match_predictions = []

st.header("Gruppekampe")
for index, row in df.iterrows():
    fixture_id = row['fixture_id']

    results = df_res[df_res["fixture_id"]==fixture_id]
    info = row["date"] + ": \n" + row["home"] + " - " + row["away"]
    results_options = results["item"].tolist()

    col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1.5, 3])
    col1.write(info)
    col2.write(row["1"])
    col3.write(row["X"])
    col4.write(row["2"])

    with col5:
        match_prediction = st.selectbox("Dit bud", options=result_choices, key=fixture_id)
    with col6:
        result_prediction = st.selectbox("Resultat", options=results_options, key=f"result_{fixture_id}")

    match_predictions.append({'fixture_id': fixture_id, 'prediction': match_prediction, 'result_prediction': result_prediction})

predictions_df = pd.DataFrame(match_predictions)

st.header("Vinder")
df_winner = pd.read_csv('Webapp/winner.csv')
winner_prediction = st.selectbox("Dit bud", options=df_winner["item"])
json_data = predictions_df.to_json(orient='records')

st.download_button(
    label="Download JSON",
    data=json_data,
    file_name='user_picks.json',
    mime='application/json',
)