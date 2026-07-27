import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

from predict import predict_function
from update import update_function

#Background Colour: Soft White
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    background-color: #FBFAF5 !important;
}


</style>
""", unsafe_allow_html=True)
#Selection Box Colours
st.markdown("""
<style>

div[data-testid="stSelectbox"] > label {
    color: #000000 !important; 
}

div[data-baseweb="select"] > div {
    color: #FFFFFF !important;  
}

ul[data-baseweb="menu"] li {
    color: #000000 !important; 
}

ul[data-baseweb="menu"] {
    background-color: #01183F !important;
}

</style>
""", unsafe_allow_html=True)
#Button Customization
st.markdown("""
<style>
.stButton > button {
    background-color: #04AA6D !important;
    color: white !important;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 20px;
    font-weight: 600;
    transition: 0.2s ease-in-out;
}
.stButton > button:hover {
    background-color: #025f3d !important;
    color: #FFFFFF !important;
    border: 1px solid #025f3d !important; 
}
</style>
""", unsafe_allow_html=True)
#Loading Teko Font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600;700&display=swap');
</style>
""", unsafe_allow_html=True)


#Mapping
team_colors = {
    "Anaheim Ducks": "#000000",
    "Arizona Coyotes": "#8C2633",
    "Boston Bruins": "#FFB81C",
    "Buffalo Sabres": "#003087",
    "Calgary Flames": "#C8102E",
    "Carolina Hurricanes": "#CC0000",
    "Chicago Blackhawks": "#CF0A2C",
    "Colorado Avalanche": "#6F263D",
    "Columbus Blue Jackets": "#002654",
    "Dallas Stars": "#006847",
    "Detroit Red Wings": "#CE1126",
    "Edmonton Oilers": "#FF4C00",
    "Florida Panthers": "#C8102E",
    "Los Angeles Kings": "#111111",
    "Minnesota Wild": "#154734",
    "Montreal Canadiens": "#AF1E2D",
    "Nashville Predators": "#003087",
    "New Jersey Devils": "#CE1126",
    "New York Islanders": "#00529B",
    "New York Rangers": "#0038A8",
    "Ottawa Senators": "#C8102E",
    "Philadelphia Flyers": "#000000",
    "Pittsburgh Penguins": "#FCB514",
    "San Jose Sharks": "#006D75",
    "Seattle Kraken": "#99D9D9",
    "St. Louis Blues": "#002F87",
    "Tampa Bay Lightning": "#002868",
    "Toronto Maple Leafs": "#00205B",
    "Utah Mammoth": "#5A2D82",
    "Vancouver Canucks": "#003F72",
    "Vegas Golden Knights": "#B4975A",
    "Washington Capitals": "#C8102E",
    "Winnipeg Jets": "#041E42"
}


#Create 3 columns: left, right, and center. Left and Right columns are margins
left2, center2, right2 = st.columns([2, 1, 2])
left, center, right = st.columns([1, 100, 1])


#Update Data Button
load_dotenv()
password = os.getenv("MYSQL_PASSWORD")
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/oilers_game_outcome_predictor")
df = pd.read_sql("SELECT * FROM features_2", engine)
latest_date = df["date"].max().strftime("%Y-%m-%d")

with center2:
    update_button_placeholder = st.empty()
    update_pressed = update_button_placeholder.button("Update Data", use_container_width = True, key = "update_button_original")

if update_pressed:
    update_button_placeholder.button("Updating...", use_container_width = True, key = "update_button_updating")

    update_function()

    update_button_placeholder.button("Update Date", use_container_width = True, key = "update_button_back_to_original")

with center2:
    st.markdown(
        f"<p style='color:black; font-size:14.53px; text-align:center;'>Latest Game Stored: {latest_date}</p>",
        unsafe_allow_html=True
    )


#Title and Oilers Logo
with center:
    col_title, col_logo = st.columns([3, 1])

    #Logo Padding
    col_logo.markdown("<div style='padding-top: 0px; '></div>", unsafe_allow_html=True)

    #Logo
    col_logo.image(
        os.path.join(os.getcwd(), "static", "edmonton-oilers-logo.png"),
        width=148
    )

    with col_title:
        st.markdown(
            "<div style='font-family: Teko; color:#01183F; font-size: 75px; font-weight: 700;'>Edmonton Oilers</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='font-family: Teko; color:#FF4C00; font-size: 54.2px; font-weight: 600; margin-top: -30px;'>Game Outcome Predictor</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<hr style='border: none; border-top: 2px solid #BFBFBF; margin: 20px 0;'>",
        unsafe_allow_html=True
    )


#Selection Boxes
with center:
    centre_L, centre_R = st.columns([1, 1])
    with centre_L:
        opponent_selection = st.selectbox(
            "Select Opponent",
            [
                "Anaheim Ducks",
                "Arizona Coyotes",
                "Boston Bruins",
                "Buffalo Sabres",
                "Calgary Flames",
                "Carolina Hurricanes",
                "Chicago Blackhawks",
                "Colorado Avalanche",
                "Columbus Blue Jackets",
                "Dallas Stars",
                "Detroit Red Wings",
                "Edmonton Oilers",
                "Florida Panthers",
                "Los Angeles Kings",
                "Minnesota Wild",
                "Montreal Canadiens",
                "Nashville Predators",
                "New Jersey Devils",
                "New York Islanders",
                "New York Rangers",
                "Ottawa Senators",
                "Philadelphia Flyers",
                "Pittsburgh Penguins",
                "San Jose Sharks",
                "Seattle Kraken",
                "St. Louis Blues",
                "Tampa Bay Lightning",
                "Toronto Maple Leafs",
                "Utah Mammoth",
                "Vancouver Canucks",
                "Vegas Golden Knights",
                "Washington Capitals",
                "Winnipeg Jets"
            ]
        )
    with centre_R:
        home_or_away_selection = st.selectbox(
            "Are the Oilers Playing at Home or Away?",
            ["Home", "Away"]
        )

    st.markdown(
        "<hr style='border: none; border-top: 2px solid #BFBFBF; margin: 20px 0;'>",
        unsafe_allow_html=True
    )


#Predict Button
with center:
    predict_button_placeholder = st.empty()
    predict_pressed = predict_button_placeholder.button("Predict", use_container_width=True, key="predict_button_original")

    st.markdown(
        "<hr style='border: none; border-top: 2px solid #BFBFBF; margin: 20px 0;'>",
        unsafe_allow_html=True
    )

if predict_pressed:
    predict_button_placeholder.button("Predicting...", use_container_width=True, key="predict_button_predicting")

    prediction_output = predict_function(opponent_selection, home_or_away_selection)

    predict_button_placeholder.button("Predict", use_container_width=True, key="predict_button_back_to_original")

    #Win probability bar
    win = float(prediction_output[1][0:5:1])
    loss = float(prediction_output[2][0:5:1])

    with center:
        if prediction_output[0] == "L":
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <p style="color:black; font-size:30px; font-weight:bold;">
                        {opponent_selection} Win
                    </p>
                </div>
                """,
                unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <p style="color:black; font-size:30px; font-weight:bold;">
                        Edmonton Oilers Win
                    </p>
                </div>
                """,
                unsafe_allow_html=True)

        if home_or_away_selection == "Away":
            st.markdown(f"""
            <div style="
                width: 100%;
                height: 30px;
                background: linear-gradient(
                    to right,
                    #FF4C00 {win}%,   /* Oilers orange */
                    {team_colors[opponent_selection]} {win}%    
                );
                border-radius: 8px;
                margin-top: 10px;
            ">
            </div>
    
            <div style="
                display: flex;
                justify-content: space-between;
                font-size: 18px;
                color: black;
                margin-top: 5px;
            ">
                <span>Edmonton Oilers Win: {win:.1f}%</span>
                <span>{opponent_selection} Win: {loss:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                        <div style="
                            width: 100%;
                            height: 30px;
                            background: linear-gradient(
                                to left,
                                #FF4C00 {win}%,   /* Oilers orange */
                                {team_colors[opponent_selection]} {win}%    
                            );
                            border-radius: 8px;
                            margin-top: 10px;
                        ">
                        </div>

                        <div style="
                            display: flex;
                            justify-content: space-between;
                            font-size: 18px;
                            color: black;
                            margin-top: 5px;
                        ">
                            <span>{opponent_selection} Win: {loss:.1f}%</span>
                            <span>Edmonton Oilers Win: {win:.1f}%</span>
                        </div>
                        """, unsafe_allow_html=True)







