# oilers-game-outcome-predictor

An **end-to-end** machine learning project that predicts the outcome of a hypothetical future Edmonton Oilers game using hockey features engineered from past games and a Random Forest Classifier model. The app includes a Streamlit interface with prediction and database‑update functionality, backed by a local MySQL database. The codebase demonstrates practical skills in feature engineering, Scikit-Learn model training, SQL integration, and building interactive ML tools.

DEMO VIDEO: https://github.com/TaneeshChekka/oilers-game-outcome-predictor/blob/main/screenshots_and_videos/Oilers%20Predictor%20Video.mp4

## TABLE OF CONTENTS
- [Project Elements](#project-elements)
- [In this repo](#in-this-repo)
- [Stack](#stack)

##
**Streamlit UI Screenshot**
![Streamlit UI](https://github.com/TaneeshChekka/oilers-game-outcome-predictor/blob/28402689c8c6c6737163056c6259380c7442f5b4/screenshots_and_videos/After%20prediction.png)

## Project Elements

**DATA PIPELINE AND FEATURE ENGINEERING:**

This project builds a full end‑to‑end data pipeline using the NHL API Reference (https://github.com/Zmalski/NHL-API-Reference) as the data source for Edmonton Oilers game data.

- **Extraction tools:** `requests` and `pandas`
- **Storage:** Local **MySQL** database
- **Incremental updates:**  
  - `update.py` checks the latest stored game on MySQL
  - Fetches new Oilers games from the NHL API  
  - Inserts only new rows to avoid duplicates
- **Feature engineering:**  
  - Home/away indicators  
  - Opponent rolling strength metrics 
  - Normalized scoring features  
  - Win/loss labels  
  - Rolling averages and recent‑form indicators
- **Skills demonstrated:** API integration, SQL schema design, ETL pipelines, pandas transformations, and clean data engineering practices.

---

**MACHINE LEARNING MODEL:**

A Random Forest Classifier predicts the outcome of a future Oilers game using engineered features stored in MySQL.

- **Modeling tools:** `scikit-learn`, `pandas`, `numpy`
- **Training workflow:**  
  - Train/test split for evaluation  
  - Feature scaling and encoding  
  - Hyperparameter tuning using `GridSearchCV` and `RandomizedSearchCV`
- **Model inputs:**  
  - Team performance metrics  
  - Opponent rolling strength  
  - Normalized scoring features  
  - Recent‑form indicators and game context (home/away)
- **Outputs:**  
  - Binary prediction (win/loss)  
  - Probability score for model confidence
- **Skills demonstrated:** ML pipeline construction, model tuning, feature engineering, reproducible training workflow, and practical sports analytics modeling.

---

**STREAMLIT FRONT END:**

A Streamlit interface provides an interactive way to run predictions and update the database with the latest Oilers game.

- **Front‑end tools:** `streamlit`, `pandas`
- **UI features:**  
  - Selection boxes to choose Opponent and Home/Away  
  - Model prediction and probability bar display 
  - Update Database button to fetch the newest game  
- **Skills demonstrated:** Front‑end UI design, backend integration, and deploying interactive ML tools.



## In this repo:

python\_files/:

* streamlit\_app\_oilers\_predictor.py -> Streamlit interface code
* update.py -> Function to update data on SQL to the latest Oilers game
* predict.py -> Scikit-Learn machine learning model that predicts game outcome based on user inputs
* static/ -> images used in Streamlit UI

screenshots\_and\_videos/ -> screenshots and videos of Streamlit UI

SQL/:

* SQL\_schema.md -> Description of tables on SQL database

requirements.txt -> Python dependencies used by this project


## Stack

- **Python** — core language for data processing, modeling, and backend logic  
- **pandas / numpy** — data cleaning, feature engineering, and numerical operations  
- **requests** — extracting game data from the NHL API  
- **MySQL** — structured storage for raw games, engineered features, and model inputs  
- **scikit-learn** — Random Forest model, training pipeline, and hyperparameter tuning  
- **Streamlit** — front‑end UI for predictions and database updates  






