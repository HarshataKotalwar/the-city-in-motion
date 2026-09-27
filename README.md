# The City in Motion

## Understanding Urban Mobility, Demand & Trip Economics in New York City

## Project Overview

**The City in Motion** is an end-to-end data analytics project exploring urban taxi demand, trip characteristics, geographic patterns and trip economics across New York City.

Using official NYC Taxi & Limousine Commission (TLC) Yellow Taxi Trip Records, the project analyzes 12 months of trip data, from August 2025 to July 2026.

The project combines Python, DuckDB, SQL and Tableau to transform raw trip records into actionable business insights through data engineering, exploratory analysis and interactive visualization.

## Business Question

How do time, location, trip characteristics and pricing interact to shape taxi demand and trip economics across New York City?

## Business Questions

1. When does taxi demand peak?
2. How does demand vary by month, weekday and hour?
3. Which pickup zones generate the most activity?
4. Which drop-off zones receive the most trips?
5. How do trip distance and duration relate to trip amounts?
6. How does trip amount vary across time periods?
7. How do payment methods and fare components contribute to trip economics?
8. What operational patterns can be identified from the data?

## Data Source

**NYC Taxi & Limousine Commission (TLC)**

Official source: [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

### Dataset Scope

* **Period:** August 2025 – July 2026
* **Duration:** 12 months
* **Trip type:** Yellow Taxi Trip Records
* **Geographic reference:** Official NYC Taxi Zone Lookup Table

The project uses the official TLC records and taxi zone lookup to analyze trip demand, geography and trip economics.

## Analytical Workflow

```text
Official TLC Data
       |
       v
Data Inspection
       |
       v
Data Quality Assessment
       |
       v
Data Engineering
       |
       v
DuckDB Data Processing
       |
       v
SQL Analysis
       |
       v
Python EDA
       |
       v
Business Analysis
       |
       v
Tableau Dashboard
       |
       v
Business Insights
```

## Tech Stack

| Technology       | Purpose                                   |
| ---------------- | ----------------------------------------- |
| Python           | Data processing and analysis              |
| Pandas           | Data manipulation                         |
| PyArrow          | Parquet data handling                     |
| DuckDB           | Analytical data processing                |
| SQL              | Data querying and business analysis       |
| Jupyter Notebook | Exploratory data analysis                 |
| Tableau Public   | Interactive dashboard and visualization   |
| Git & GitHub     | Version control and project documentation |

## Key Findings

* **45.68 million trips** were analyzed across the 12-month period.
* **December 2025** recorded the highest monthly trip volume, with approximately 4.26 million trips.
* **6 PM** was the busiest pickup hour, with approximately 3.20 million trips.
* **Weekdays** accounted for approximately 71.66% of all trips.
* **Manhattan** accounted for the largest share of recorded pickups.
* **Upper East Side South** was the leading pickup zone by trip volume.
* Trips originating at JFK and LaGuardia airports had a higher average total trip amount than non-airport trips.

These findings are descriptive and reflect the selected dataset and analysis period. Airport trips are defined by pickups at JFK and LaGuardia.

## Tableau Dashboard

**The City in Motion — NYC Taxi Mobility Dashboard**

[View Interactive Dashboard on Tableau Public](https://public.tableau.com/app/profile/harshata.kotalwar/viz/The_city_in_motion_/Dashboard1)
## Dashboard Preview

Explore **The City in Motion**, an interactive Tableau dashboard analyzing NYC Yellow Taxi trips from August 2025 to July 2026.

![The City in Motion Dashboard](the_city_in_motion.png)
The dashboard includes:

* Overall trip volume and demand indicators
* Monthly and hourly demand trends
* Weekday versus weekend demand
* Borough-level pickup distribution
* Top 10 pickup and drop-off zones
* Monthly average trip amount
* Airport versus non-airport trip comparisons

## Project Structure

```text
the-city-in-motion/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── dashboard/
│   └── data/
│
├── docs/
│   ├── Business_Questions.md
│   ├── Data_Dictionary.md
│   ├── Data_Model.md
│   ├── Data_Quality_Report.md
│   ├── Data_Source.md
│   ├── Executive_Summary.md
│   └── Project_Charter.md
│
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   ├── 02_eda.ipynb
│   └── 03_business_analysis.ipynb
│
├── reports/
│   ├── analysis/
│   └── data_quality_report.json
│
├── scripts/
│   ├── create_derived_features.py
│   ├── data_quality.py
│   ├── inspect_data.py
│   └── process_data.py
│
├── sql/
│   ├── business_questions.sql
│   ├── data_quality.sql
│   ├── demand_analysis.sql
│   ├── location_analysis.sql
│   ├── revenue_analysis.sql
│   └── trip_economics.sql
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Project Limitations

* The analysis is limited to the selected 12-month period and Yellow Taxi records.
* Trip amounts represent recorded trip amounts and should not be interpreted as net business revenue.
* Airport trips are defined using JFK and LaGuardia pickup locations.
* The findings describe observed patterns and do not establish causal relationships.

## Future Improvements

* Add interactive filters for more detailed geographic and temporal analysis.
* Explore predictive models for taxi demand.
* Investigate demand patterns at a more granular geographic level.
* Extend the analysis to additional taxi services or periods.
