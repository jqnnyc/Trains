import pandas as pd
from trainAPI import *
import streamlit as st
from streamlit_TTS import text_to_speech

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

def on_select_change():
    text = f"Sweary Trains Incorporated presents the fucking upcoming departure times from {loc_label} train station."
    text_to_speech(text)
    text = f"What an absolute shit hole that place is."
    text_to_speech(text)
    text = f"And you are a bell end."
    text_to_speech(text)

# Create a selectbox with labels
loc_label = st.selectbox("Select a station (if you want, you twat)", options.values(), index=list(options.keys()).index('FLE'),on_change=on_select_change)

# Get the corresponding key
loc = [key for key, value in options.items() if value == loc_label][0]

df, df2 = returnTrains(loc)

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
        df, df2 = returnTrains(loc)

    t = df[['std','etd','destination','platform']]
    t = t.rename(columns={'std': 'Scheduled', 'etd': 'Estimated', 'destination': 'Destination', 'platform': 'Platform'})
    st.dataframe(t)

    df2['Service'] = df2['std'] + ' to ' + df2['destination']
    services = df2['Service'].unique()
    serviceSelect = st.selectbox("Where does it fucking stop?", services)
    selectedService = df2[df2['Service'] == serviceSelect]
    selectedService_print = selectedService[['locationName','st','et']].reset_index(drop=True)
    selectedService_print = selectedService_print.rename(columns={'locationName': 'Calling Point', 'st': 'Scheduled', 'et': 'Estimated'})
    st.dataframe(selectedService_print)






