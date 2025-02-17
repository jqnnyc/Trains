import pandas as pd
from trainAPI import *
import streamlit as st

df = returnTrains("FLE")

button_run_pressed = st.button("Reload the fucking data")
if button_run_pressed:
    df = returnTrains("FLE")

st.title("Fucking Trains")

st.markdown("Showing the next few fucking trains from pissing Fleet train station for your pleasure. You wanker.")

st.markdown(f"The next train is to the shithole of **{df.at[0,"destination"]}** at **{df.at[0, "std"]}**. It is currently due {df.at[0, "etd"]}. Hope it's your train you twat.")

st.markdown(f"After that you can piss off to **{df.at[1,"destination"]}** if you're that way inclined. That train is scheduled at **{df.at[1, "std"]}** and i'm not telling you if it's on time because i think you're a prick.")

st.markdown("Oh you want more? Well here's the fucking departure board:")

st.write(df.head())

