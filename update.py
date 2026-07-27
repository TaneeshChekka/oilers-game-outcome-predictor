def update_function():
    import numpy as np
    import pandas as pd
    from datetime import datetime
    from datetime import date
    import requests
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv

    #functions (used later in script)
    def api_season_select():
        year = datetime.now().year
        month = datetime.now().strftime("%m")
        if int(month) <= 8:
            season_code = str(int(year)-1)+str(year)
        else:
            season_code = str(year)+str(int(year)+1)
        return season_code
    def home_away(row_df):
        if row_df["home_team"] == "Oilers":
            return "Home"
        else:
            return "Away"
    def find_opponent(row_df):
        if row_df["home_or_away"] == "Home":
            return row_df["away_team"]
        else:
            return row_df["home_team"]
    def find_opponent_abbrev(row_df):
        if row_df["home_or_away"] == "Home":
            return row_df["awayTeam_abbrev"]
        else:
            return row_df["homeTeam_abbrev"]
    def oilers_score(row_df):
        if row_df["home_or_away"] == "Home":
            return row_df["home_team_score"]
        else:
            return row_df["away_team_score"]
    def opponent_score(row_df):
        if row_df["home_or_away"] == "Home":
            return row_df["away_team_score"]
        else:
            return row_df["home_team_score"]
    def win_loss(row_df):
        if row_df["oilers_score"] > row_df["opponent_score"]:
            return "W"
        else:
            return "L"
    def opponent_last_5_goals_mean(row_df):
        #Cache schedules
        i = (str(row_df["opponent_abbrev"]), str(row_df["season"]))
        if i not in opponent_data_cache:
           api_url = "https://api-web.nhle.com/v1/club-schedule-season/{}/{}".format(str(row_df["opponent_abbrev"]), str(row_df["season"]))
           api_data = requests.get(api_url).json()
           df_games = pd.json_normalize(api_data["games"], sep="_")
           df_games["gameDate"] = pd.to_datetime(df_games["gameDate"])
           df_games = df_games[df_games["gameDate"] < today]
           df_games["score"] = df_games.apply(lambda row:
                                              row["awayTeam_score"] if row_df["opponent_abbrev"] == row["awayTeam_abbrev"]
                                              else row["homeTeam_score"], axis=1)
           df_games["win_binary"] = df_games.apply(lambda row:
                                                   1 if
                                                   (row["awayTeam_score"] > row["homeTeam_score"] and row_df["opponent_abbrev"] == row["awayTeam_abbrev"])
                                                   or
                                                   (row["homeTeam_score"] > row["awayTeam_score"] and row_df["opponent_abbrev"] == row["homeTeam_abbrev"])
                                                   else
                                                   0,
                                                   axis=1
                                                   )
           opponent_data_cache[i] = df_games
        else:
            df_games = opponent_data_cache[i]

        df_games = df_games[df_games["gameDate"] < row_df["date"]]
        df_games_last5 = df_games.tail(5).copy()

        output = df_games_last5["score"].mean()

        return output
    def opponent_last_5_win_rate(row_df):
        #Cache schedules
        i = (str(row_df["opponent_abbrev"]), str(row_df["season"]))
        if i not in opponent_data_cache:
           api_url = "https://api-web.nhle.com/v1/club-schedule-season/{}/{}".format(str(row_df["opponent_abbrev"]), str(row_df["season"]))
           api_data = requests.get(api_url).json()
           df_games = pd.json_normalize(api_data["games"], sep="_")
           df_games["gameDate"] = pd.to_datetime(df_games["gameDate"])
           df_games = df_games[df_games["gameDate"] < today]
           df_games["score"] = df_games.apply(lambda row:
                                              row["awayTeam_score"] if row_df["opponent_abbrev"] == row["awayTeam_abbrev"]
                                              else row["homeTeam_score"], axis=1)
           df_games["win_binary"] = df_games.apply(lambda row:
                                                   1 if
                                                   (row["awayTeam_score"] > row["homeTeam_score"] and row_df["opponent_abbrev"] == row["awayTeam_abbrev"])
                                                   or
                                                   (row["homeTeam_score"] > row["awayTeam_score"] and row_df["opponent_abbrev"] == row["homeTeam_abbrev"])
                                                   else
                                                   0,
                                                   axis=1
                                                   )
           opponent_data_cache[i] = df_games
        else:
            df_games = opponent_data_cache[i]

        df_games = df_games[df_games["gameDate"] < row_df["date"]]
        df_games_last5 = df_games.tail(5).copy()

        output = df_games_last5["win_binary"].mean()

        return output
    def oilers_last_2_win_rate_vs_opponent(row_df):
        features_1_opponent_only = features_1[features_1["opponent_abbrev"] == row_df["opponent_abbrev"]]
        features_1_opponent_only = features_1_opponent_only[features_1_opponent_only["date"] < row_df["date"]]
        features_1_opponent_only_last2 = features_1_opponent_only.tail(2).copy()

        if features_1_opponent_only_last2.empty:
            return np.nan
        else:
            return features_1_opponent_only_last2["win_binary"].mean()
    def oilers_last_2_goals_mean_vs_opponent(row_df):
        features_1_opponent_only = features_1[features_1["opponent_abbrev"] == row_df["opponent_abbrev"]]
        features_1_opponent_only = features_1_opponent_only[features_1_opponent_only["date"] < row_df["date"]]
        features_1_opponent_only_last2 = features_1_opponent_only.tail(2).copy()

        if features_1_opponent_only_last2.empty:
            return np.nan
        else:
            return features_1_opponent_only_last2["oilers_score"].mean()
    def oilers_last_2_goals_let_in_mean_vs_opponent(row_df):
        features_1_opponent_only = features_1[features_1["opponent_abbrev"] == row_df["opponent_abbrev"]]
        features_1_opponent_only = features_1_opponent_only[features_1_opponent_only["date"] < row_df["date"]]
        features_1_opponent_only_last2 = features_1_opponent_only.tail(2).copy()

        if features_1_opponent_only_last2.empty:
            return np.nan
        else:
            return features_1_opponent_only_last2["opponent_score"].mean()
    def oilers_last_2_goal_differential_mean_vs_opponent(row_df):
        features_1_opponent_only = features_1[features_1["opponent_abbrev"] == row_df["opponent_abbrev"]]
        features_1_opponent_only = features_1_opponent_only[features_1_opponent_only["date"] < row_df["date"]]
        features_1_opponent_only_last2 = features_1_opponent_only.tail(2).copy()

        if features_1_opponent_only_last2.empty:
            return np.nan
        else:
            return features_1_opponent_only_last2["goal_differential"].mean()


    #-----------------------------------------------------------------


    today = pd.to_datetime(date.today())
    opponent_data_cache = {}

    #read features_1 table on SQL and find most recent game date
    load_dotenv()
    password = os.getenv("MYSQL_PASSWORD")
    engine  = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/oilers_game_outcome_predictor")
    features_1 = pd.read_sql("SELECT * FROM features_1", engine)
    maxdate_features_1 = features_1["date"].max()

    #pull data from API (only games not in features_1 on SQL)
    oilers_api_url = "https://api-web.nhle.com/v1/club-schedule-season/EDM/" + str(api_season_select())
    oilers_api_data = requests.get(oilers_api_url).json()
    oilers_api_df_games = pd.json_normalize(oilers_api_data["games"], sep="_")
    oilers_api_df_games["gameDate"] = pd.to_datetime(oilers_api_df_games["gameDate"])
    oilers_api_df_games = oilers_api_df_games[oilers_api_df_games["gameDate"] > maxdate_features_1]
    oilers_api_df_games = oilers_api_df_games[oilers_api_df_games["gameDate"] < today]
    dataframe = oilers_api_df_games[[
        "id",
        "season",
        "gameDate",
        "awayTeam_commonName_default",
        "awayTeam_abbrev",
        "awayTeam_score",
        "homeTeam_commonName_default",
        "homeTeam_abbrev",
        "homeTeam_score",
        "periodDescriptor_periodType"
    ]]
    dataframe = dataframe.rename(columns={
        "gameDate" : "date",
        "awayTeam_commonName_default" : "away_team",
        "awayTeam_score" : "away_team_score",
        "homeTeam_commonName_default" : "home_team",
        "homeTeam_score" : "home_team_score",
        "periodDescriptor_periodType" : "reg/ot"
    })

    #Feature engineering 1
    dataframe["home_or_away"] = dataframe.apply(lambda row_df: home_away(row_df), axis=1)
    dataframe["opponent"] = dataframe.apply(lambda row_df: find_opponent(row_df), axis=1)
    dataframe["opponent_abbrev"] = dataframe.apply(lambda row_df: find_opponent_abbrev(row_df), axis=1)
    dataframe["oilers_score"] = dataframe.apply(lambda row_df: oilers_score(row_df), axis=1)
    dataframe["opponent_score"] = dataframe.apply(lambda row_df: opponent_score(row_df), axis=1)
    dataframe["win_or_loss"] = dataframe.apply(lambda row_df: win_loss(row_df), axis=1)
    dataframe = dataframe.drop(["away_team_score", "home_team_score", "away_team", "home_team", "awayTeam_abbrev", "homeTeam_abbrev"], axis=1)
    dataframe["date"] = pd.to_datetime(dataframe["date"])

    #store in SQL to features_1 table
    dataframe.to_sql("features_1", engine, if_exists = "append")

    #read appended features_1
    features_1 = pd.read_sql("SELECT * FROM features_1", engine)
    features_1 = features_1.sort_values(by="date", ascending=True)

    #Feature engineering 2
    features_1["last_5_game_goals_mean"] = features_1["oilers_score"].shift(1).rolling(window = 5, min_periods = 1).mean()
    features_1["last_2_game_goals_mean"] = features_1["oilers_score"].shift(1).rolling(window = 2, min_periods = 1).mean()
    features_1["last_5_game_goals_let_in_mean"] = features_1["opponent_score"].shift(1).rolling(window = 5, min_periods = 1).mean()
    features_1["last_2_game_goals_let_in_mean"] = features_1["opponent_score"].shift(1).rolling(window = 2, min_periods = 1).mean()

    features_1["win_binary"] = features_1["win_or_loss"].apply(lambda x: 1 if x == "W" else 0)
    features_1["last_5_game_win_rate"] = features_1["win_binary"].shift(1).rolling(window = 5, min_periods = 1).mean()
    features_1["last_2_game_win_rate"] = features_1["win_binary"].shift(1).rolling(window = 2, min_periods = 1).mean()
    features_1["season_win_rate_expanding"] = features_1.groupby("season")["win_binary"].expanding().mean().reset_index(level = 0, drop = True).groupby(features_1["season"]).shift(1)
    features_1["season_win_rate_expanding"] = features_1["season_win_rate_expanding"].fillna(0).astype(float)
    features_1["season_games_played"] = features_1.groupby("season")["id"].expanding().count().reset_index(level = 0, drop = True).groupby(features_1["season"]).shift(1)
    features_1["season_games_played"] = features_1["season_games_played"].fillna(0).astype(float)

    features_1["goal_differential"] = features_1["oilers_score"] - features_1["opponent_score"]
    features_1["last_5_game_goal_differential_mean"] = features_1["goal_differential"].shift(1).rolling(window = 5, min_periods = 1).mean()
    features_1["last_2_game_goal_differential_mean"] = features_1["goal_differential"].shift(1).rolling(window = 2, min_periods = 1).mean()

    #Filter to only have games not in features_2 on SQL
    features_2 = pd.read_sql("SELECT * FROM features_2", engine)
    maxdate_features_2 = features_2["date"].max()
    features_1 = features_1[features_1["date"] > maxdate_features_2]

    #Opponent features
    if not(features_1.empty):
        features_1["opponent_last_5_game_goals_mean"] = features_1.apply(lambda row_df: opponent_last_5_goals_mean(row_df), axis=1)
        features_1["opponent_last_5_win_rate"] = features_1.apply(lambda row_df: opponent_last_5_win_rate(row_df), axis=1)
        features_1["oilers_last_2_win_rate_vs_opponent"] = features_1.apply(lambda row_df: oilers_last_2_win_rate_vs_opponent(row_df), axis=1)
        features_1["oilers_last_2_goals_mean_vs_opponent"] = features_1.apply(lambda row_df: oilers_last_2_goals_mean_vs_opponent(row_df), axis=1)
        features_1["oilers_last_2_goals_let_in_mean_vs_opponent"] = features_1.apply(lambda row_df: oilers_last_2_goals_let_in_mean_vs_opponent(row_df), axis=1)
        features_1["oilers_last_2_goal_differential_mean_vs_opponent"] = features_1.apply(lambda row_df: oilers_last_2_goal_differential_mean_vs_opponent(row_df), axis=1)

    #Drop unnecessary columns
    features_1 = features_1.drop("win_binary", axis = 1)
    features_1 = features_1.drop("goal_differential", axis = 1)
    features_1 = features_1.drop("index", axis = 1)

    #store in SQL to features_2 table
    features_1.to_sql("features_2", engine, if_exists = "append")


