## SQL Database Schema

This project uses a local MySQL database with two main tables.

---

## **features_1**

Raw and intermediate engineered features for past Edmonton Oilers games.

### **Columns**
- `index` (BIGINT)
- `id` (BIGINT)
- `season` (BIGINT)
- `date` (DATETIME)
- `reg/ot` (TEXT)
- `home_or_away` (TEXT)
- `opponent` (TEXT)
- `opponent_abbrev` (TEXT)
- `oilers_score` (BIGINT)
- `opponent_score` (BIGINT)
- `win_or_loss` (TEXT)

This table is appended and updated inside `update.py`.

---

## **features_2**

Final engineered feature set used for model training and prediction.

### **Columns carried from `features_1`**
- `index` (BIGINT)
- `id` (BIGINT)
- `season` (BIGINT)
- `date` (DATETIME)
- `reg/ot` (TEXT)
- `home_or_away` (TEXT)
- `opponent` (TEXT)
- `opponent_abbrev` (TEXT)
- `oilers_score` (BIGINT)
- `opponent_score` (BIGINT)
- `win_or_loss` (TEXT)

### **Engineered Features**
- `last_5_game_goals_mean` (DOUBLE)
- `last_2_game_goals_mean` (DOUBLE)
- `last_5_game_goals_let_in_mean` (DOUBLE)
- `last_2_game_goals_let_in_mean` (DOUBLE)
- `last_5_game_win_rate` (DOUBLE)
- `last_2_game_win_rate` (DOUBLE)
- `season_win_rate_expanding` (DOUBLE)
- `season_games_played` (DOUBLE)
- `last_5_game_goal_differential_mean` (DOUBLE)
- `last_2_game_goal_differential_mean` (DOUBLE)
- `opponent_last_5_game_goals_mean` (DOUBLE)
- `opponent_last_5_win_rate` (DOUBLE)
- `oilers_last_2_win_rate_vs_opponent` (DOUBLE)
- `oilers_last_2_goals_mean_vs_opponent` (DOUBLE)
- `oilers_last_2_goals_let_in_mean_vs_opponent` (DOUBLE)
- `oilers_last_2_goal_differential_mean_vs_opponent` (DOUBLE)

This table is created by filtering and enhancing `features_1` inside `update.py`.

---

### **Notes**
- The database is **local only** and not included in this repository.
- No credentials or actual data are stored in GitHub.
