# Bank Marketing Campaign Analysis

An exploratory data analysis project using a real marketing campaign dataset from the UCI Machine Learning Repository. The dataset contains 45,211 phone-based marketing contacts made by a Portuguese bank to promote term deposits.

## Business questions

- Which customer segments have the highest campaign conversion rate?
- Which contact methods and months perform best?
- How does the number of contacts affect conversion?
- How can campaign teams prioritize future outreach?

## Tools

Python, Pandas, NumPy, Matplotlib, SQL

## Workflow

1. Load and validate the semicolon-delimited source data.
2. Check missing values, data types, and target balance.
3. Calculate conversion rates by job, education, age group, contact method, month, and campaign contacts.
4. Export summary tables for dashboarding.
5. Produce recommendations based on observed conversion patterns.

## Run locally

```bash
pip install -r requirements.txt
python analysis.py
```

## Data source

UCI Machine Learning Repository - Bank Marketing dataset:
https://archive.ics.uci.edu/dataset/222/bank+marketing

The dataset is licensed under CC BY 4.0. The original data is retained in `data/raw/` for reproducibility.
