This project uses a local MySQL database with two main tables:



\---



\## features\_1

Raw and intermediate engineered features for past Edmonton Oilers games.



\### Columns

\- index (BIGINT)

\- id (BIGINT)

\- season (BIGINT)

\- date (DATETIME)

\- reg/ot (TEXT)

\- home\_or\_away (TEXT)

\- opponent (TEXT)

\- opponent\_abbrev (TEXT)

\- oilers\_score (BIGINT)

\- opponent\_score (BIGINT)

\- win\_or\_loss (TEXT)



This table is appended and updated inside `update.py`.



\---



\## features\_2

Final engineered feature set used for model training and prediction.



\### Columns carried from `features\_1`

\- index (BIGINT)

\- id (BIGINT)

\- season (BIGINT)

\- date (DATETIME)

\- reg/ot (TEXT)

\- home\_or\_away (TEXT)

\- opponent (TEXT)

\- opponent\_abbrev (TEXT)

\- oilers\_score (BIGINT)

\- opponent\_score (BIGINT)

\- win\_or\_loss (TEXT)



\### Engineered Features

\- last\_5\_game\_goals\_mean (DOUBLE)

\- last\_2\_game\_goals\_mean (DOUBLE)

\- last\_5\_game\_goals\_let\_in\_mean (DOUBLE)

\- last\_2\_game\_goals\_let\_in\_mean (DOUBLE)

\- last\_5\_game\_win\_rate (DOUBLE)

\- last\_2\_game\_win\_rate (DOUBLE)

\- season\_win\_rate\_expanding (DOUBLE)

\- season\_games\_played (DOUBLE)

\- last\_5\_game\_goal\_differential\_mean (DOUBLE)

\- last\_2\_game\_goal\_differential\_mean (DOUBLE)

\- opponent\_last\_5\_game\_goals\_mean (DOUBLE)

\- opponent\_last\_5\_win\_rate (DOUBLE)

\- oilers\_last\_2\_win\_rate\_vs\_opponent (DOUBLE)

\- oilers\_last\_2\_goals\_mean\_vs\_opponent (DOUBLE)

\- oilers\_last\_2\_goals\_let\_in\_mean\_vs\_opponent (DOUBLE)

\- oilers\_last\_2\_goal\_differential\_mean\_vs\_opponent (DOUBLE)



This table is created by filtering and enhancing `features\_1` inside `update.py`.



\---



\### Notes

\- The database is \*\*local only\*\* and not included in this repository.

\- No credentials or actual data are stored in GitHub.



