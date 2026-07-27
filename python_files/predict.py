def predict_function(opponent, home_or_away):
    import pandas as pd
    import numpy as np
    from datetime import datetime
    from datetime import date


    #functions
    def season_select():
        year = datetime.now().year
        month = datetime.now().strftime("%m")
        if int(month) <= 8:
            season_code = str(int(year) - 1) + str(year)
        else:
            season_code = str(year) + str(int(year) + 1)
        return int(season_code)

    #mapping
    teams_name_to_abbrev = {
        # Pacific Div
        "Oilers": "EDM",
        "Edmonton": "EDM",
        "Edmonton Oilers": "EDM",

        "Flames": "CGY",
        "Calgary": "CGY",
        "Calgary Flames": "CGY",

        "Canucks": "VAN",
        "Vancouver": "VAN",
        "Vancouver Canucks": "VAN",

        "Kraken": "SEA",
        "Seattle": "SEA",
        "Seattle Kraken": "SEA",

        "Golden Knights": "VGK",
        "Vegas": "VGK",
        "Vegas Golden Knights": "VGK",

        "Kings": "LAK",
        "Los Angeles": "LAK",
        "LA": "LAK",
        "Los Angeles Kings": "LAK",

        "Ducks": "ANA",
        "Anaheim": "ANA",
        "Anaheim Ducks": "ANA",

        "Sharks": "SJS",
        "San Jose": "SJS",
        "San Jose Sharks": "SJS",

        # Central Div
        "Avalanche": "COL",
        "Colorado": "COL",
        "Colorado Avalanche": "COL",

        "Stars": "DAL",
        "Dallas": "DAL",
        "Dallas Stars": "DAL",

        "Wild": "MIN",
        "Minnesota": "MIN",
        "Minnesota Wild": "MIN",

        "Jets": "WPG",
        "Winnipeg": "WPG",
        "Winnipeg Jets": "WPG",

        "Predators": "NSH",
        "Nashville": "NSH",
        "Nashville Predators": "NSH",

        "Blues": "STL",
        "St. Louis": "STL",
        "St Louis": "STL",
        "St. Louis Blues": "STL",

        "Blackhawks": "CHI",
        "Chicago": "CHI",
        "Chicago Blackhawks": "CHI",

        "Coyotes": "ARI",
        "Arizona": "ARI",
        "Arizona Coyotes": "ARI",

        "Mammoth": "UTA",
        "Utah": "UTA",
        "Utah Mammoth": "UTA",

        # Atlantic Div
        "Bruins": "BOS",
        "Boston": "BOS",
        "Boston Bruins": "BOS",

        "Sabres": "BUF",
        "Buffalo": "BUF",
        "Buffalo Sabres": "BUF",

        "Panthers": "FLA",
        "Florida": "FLA",
        "Florida Panthers": "FLA",

        "Lightning": "TBL",
        "Tampa Bay": "TBL",
        "Tampa": "TBL",
        "Tampa Bay Lightning": "TBL",

        "Maple Leafs": "TOR",
        "Leafs": "TOR",
        "Toronto": "TOR",
        "Toronto Maple Leafs": "TOR",

        "Senators": "OTT",
        "Ottawa": "OTT",
        "Ottawa Senators": "OTT",

        "Red Wings": "DET",
        "Detroit": "DET",
        "Detroit Red Wings": "DET",

        "Canadiens": "MTL",
        "Habs": "MTL",
        "Montreal": "MTL",
        "Montreal Canadiens": "MTL",

        # Metropolitan Div
        "Rangers": "NYR",
        "New York Rangers": "NYR",

        "Islanders": "NYI",
        "New York Islanders": "NYI",

        "Devils": "NJD",
        "New Jersey": "NJD",
        "New Jersey Devils": "NJD",

        "Flyers": "PHI",
        "Philadelphia": "PHI",
        "Philadelphia Flyers": "PHI",

        "Penguins": "PIT",
        "Pittsburgh": "PIT",
        "Pittsburgh Penguins": "PIT",

        "Capitals": "WSH",
        "Washington": "WSH",
        "Washington Capitals": "WSH",

        "Hurricanes": "CAR",
        "Carolina": "CAR",
        "Carolina Hurricanes": "CAR",

        "Blue Jackets": "CBJ",
        "Columbus": "CBJ",
        "Columbus Blue Jackets": "CBJ"
    }

    #Read features_2 as the training data
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv
    load_dotenv()
    password = os.getenv("MYSQL_PASSWORD")
    engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/oilers_game_outcome_predictor")
    features_2 = pd.read_sql("SELECT * FROM features_2", engine)

    X_train = features_2.drop(["index", "id", "season", "date", "reg/ot", "opponent", "opponent_abbrev", "oilers_score", "opponent_score", "win_or_loss"],
                        axis = 1)
    y_train = features_2["win_or_loss"]

    #Create testing data
    test_df_dictionary = {"home_or_away": [home_or_away]}
    test_df = pd.DataFrame(test_df_dictionary)

    features_2["win_binary"] = features_2["win_or_loss"].apply(lambda x: 1 if x == "W" else 0)
    features_2["goal_differential"] = features_2["oilers_score"] - features_2["opponent_score"]

    features_2_tail = features_2.tail(5).copy()
    features_2_last2 = features_2.tail(2).copy()

    features_2_season = features_2[features_2["season"] == season_select()]

    test_df["last_5_game_goals_mean"] = features_2_tail["oilers_score"].mean()
    test_df["last_2_game_goals_mean"] = features_2_last2["oilers_score"].mean()
    test_df["last_5_game_goals_let_in_mean"] = features_2_tail["opponent_score"].mean()
    test_df["last_2_game_goals_let_in_mean"] = features_2_last2["opponent_score"].mean()
    test_df["last_5_game_win_rate"] = features_2_tail["win_binary"].mean()
    test_df["last_2_game_win_rate"] = features_2_last2["win_binary"].mean()

    if features_2_season.empty:
        test_df["season_win_rate_expanding"] = 0
        test_df["season_games_played"] = 0
    else:
        test_df["season_win_rate_expanding"] = features_2_season["win_binary"].mean()
        test_df["season_games_played"] = features_2_season["win_binary"].count()

    test_df["last_5_game_goal_differential_mean"] = features_2_tail["goal_differential"].mean()
    test_df["last_2_game_goal_differential_mean"] = features_2_last2["goal_differential"].mean()

    import requests
    today = pd.to_datetime(date.today())
    opponent_api_url = "https://api-web.nhle.com/v1/club-schedule-season/{}/{}".format(teams_name_to_abbrev[opponent], season_select())
    opponent_data = requests.get(opponent_api_url).json()
    opponent_df = pd.json_normalize(opponent_data["games"], sep="_")
    if opponent_df.empty:
        opponent_df = pd.DataFrame()
    else:
        opponent_df["gameDate"] = pd.to_datetime(opponent_df["gameDate"])
        opponent_df = opponent_df[opponent_df["gameDate"] < today]
        if opponent_df.empty:
            opponent_df = pd.DataFrame()
        else:
            opponent_df["score"] = opponent_df.apply(lambda row:
                                               row["awayTeam_score"] if teams_name_to_abbrev[opponent] == row["awayTeam_abbrev"]
                                               else row["homeTeam_score"], axis=1)
            opponent_df["win_binary"] = opponent_df.apply(lambda row:
                                                    1 if
                                                    (row["awayTeam_score"] > row["homeTeam_score"] and teams_name_to_abbrev[opponent] ==
                                                     row["awayTeam_abbrev"])
                                                    or
                                                    (row["homeTeam_score"] > row["awayTeam_score"] and teams_name_to_abbrev[opponent] ==
                                                     row["homeTeam_abbrev"])
                                                    else
                                                    0,
                                                    axis=1
                                                    )
            opponent_df = opponent_df.sort_values(by = "gameDate", ascending = True)

    opponent_df_tail = opponent_df.tail(5).copy()

    if opponent_df_tail.empty:
        test_df["opponent_last_5_game_goals_mean"] = np.nan
        test_df["opponent_last_5_win_rate"] = np.nan
    else:
        test_df["opponent_last_5_game_goals_mean"] = opponent_df_tail["score"].mean()
        test_df["opponent_last_5_win_rate"] = opponent_df_tail["win_binary"].mean()

    features_2_vs_opponent = features_2[features_2["opponent_abbrev"] == teams_name_to_abbrev[opponent]]
    features_2_vs_opponent_last2 = features_2_vs_opponent.tail(2).copy()

    if features_2_vs_opponent_last2.empty:
        test_df["oilers_last_2_win_rate_vs_opponent"] = np.nan
        test_df["oilers_last_2_goals_mean_vs_opponent"] = np.nan
        test_df["oilers_last_2_goals_let_in_mean_vs_opponent"] = np.nan
        test_df["oilers_last_2_goal_differential_mean_vs_opponent"] = np.nan
    else:
        test_df["oilers_last_2_win_rate_vs_opponent"] = features_2_vs_opponent_last2["win_binary"].mean()
        test_df["oilers_last_2_goals_mean_vs_opponent"] = features_2_vs_opponent_last2["oilers_score"].mean()
        test_df["oilers_last_2_goals_let_in_mean_vs_opponent"] = features_2_vs_opponent_last2["opponent_score"].mean()
        test_df["oilers_last_2_goal_differential_mean_vs_opponent"] = features_2_vs_opponent_last2["goal_differential"].mean()



    X_test = test_df



    #Numeric and Categorical Columns
    num_cols = [
        "last_5_game_goals_mean",
        "last_2_game_goals_mean",
        "last_5_game_goals_let_in_mean",
        "last_2_game_goals_let_in_mean",
        "last_5_game_win_rate",
        "last_2_game_win_rate",
        "season_win_rate_expanding",
        "season_games_played",
        "last_5_game_goal_differential_mean",
        "last_2_game_goal_differential_mean",
        "opponent_last_5_game_goals_mean",
        "opponent_last_5_win_rate",
        "oilers_last_2_win_rate_vs_opponent",
        "oilers_last_2_goals_mean_vs_opponent",
        "oilers_last_2_goals_let_in_mean_vs_opponent",
        "oilers_last_2_goal_differential_mean_vs_opponent"
    ]

    cat_cols = ["home_or_away"]

    #Numeric and categorical pipelines

    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import OneHotEncoder

    num_pipeline = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="mean")),
        ("scale", MinMaxScaler(feature_range=(0, 1))),
    ])

    cat_pipeline = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    #Column transformer
    from sklearn.compose import make_column_transformer

    col_transformer = make_column_transformer(
        (num_pipeline, num_cols),
        (cat_pipeline, cat_cols)
    )

    #Classifier model
    from sklearn.ensemble import RandomForestClassifier
    rfc = RandomForestClassifier(
        n_estimators=100,
        min_samples_split=4,
        min_samples_leaf=10,
        max_features="sqrt",
        max_depth=5,
        bootstrap=True,
        random_state=42
    )

    #Pipeline Final
    from sklearn.pipeline import make_pipeline
    pipeline_final = make_pipeline(col_transformer, rfc)
    pipeline_final.fit(X_train, y_train)

    y_pred = pipeline_final.predict(X_test)
    y_pred_proba = pipeline_final.predict_proba(X_test)

    y_pred = y_pred[0]
    prob_L, prob_W = pipeline_final.predict_proba(X_test)[0]
    prob_L = f"{prob_L:.2%}"
    prob_W = f"{prob_W:.2%}"

    return [y_pred, prob_W, prob_L]



