# oilers-game-outcome-predictor

A machine learning project that predicts the outcome of a hypothetical future Edmonton Oilers game using hockey features engineered from past games and a Random Forest Classifier model. The app includes a Streamlit interface with prediction and database‑update functionality, backed by a local MySQL database. The codebase demonstrates practical skills in feature engineering, Scikit-Learn model training, SQL integration, and building interactive ML tools.



In this repo:

streamlit\_app\_oilers\_predictor.py -> Streamlit interface code

update.py -> Function to update data on SQL to the latest Oilers game

predict.py -> Scikit-Learn machine learning model that predicts game outcome based on user inputs

requirements.txt -> Python dependencies used by this project

SQL\_schema.md -> Description of tables on SQL database

screenshots/ -> screenshots of Streamlit UI

static/ -> images used in Streamlit UI

