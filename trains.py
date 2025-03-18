import pandas as pd
from trainAPI import *
import streamlit as st

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sweary Trains:middle_finger:")

try:
    s = returnStations()
    options = dict(zip(s['crsCode'], s['stationName']))

# Define key-value pairs
except:
    options = {
        "FLE": "Fleet",
        "HOK": "Hook",
        "WAT": "Waterloo",
        "BSK": "Basingstoke",
        "SND": "Sandhurst"  
    }

# Create a selectbox with labels
loc_label = st.selectbox("Select a station (if you want, you twat)", options.values(), index=list(options.keys()).index('FLE'))

# Get the corresponding key
loc = [key for key, value in options.items() if value == loc_label][0]

df = returnTrains(loc)


if df.empty:
    st.error(f"Uh oh... looks like there are no fucking trains from {loc_label}!!")
else:
    st.success(f"Showing the next few fucking trains from pissing {loc_label} train station for your pleasure. You wanker.")

    st.markdown(f":steam_locomotive: The next train is to the shithole of **{df.at[0,'destination']}** at **{df.at[0, 'std']}**. It is currently due to be {df.at[0, 'etd'].lower()}. Hope it's your train you twat.")

    if len(df) > 1:
        st.markdown(f":steam_locomotive: After that you can piss off to **{df.at[1,'destination']}** if you're that way inclined. That train is scheduled at **{df.at[1, 'std']}** and i'm not telling you if it's on time because i think you're a prick.")
    else:
        st.error(":steam_locomotive: After that, there are no more fucking trains in the next couple of hours. Bad luck bellend!")

    st.markdown("Here's the fucking departure board:")

    button_run_pressed = st.button("Reload the fucking data")
    if button_run_pressed:
        df = returnTrains(loc)

    t = df[['std','etd','destination','platform']]
    st.dataframe(t)





