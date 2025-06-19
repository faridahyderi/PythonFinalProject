# MLB Web Scraping and Dashboard Project

This project scrapes Major League Baseball data from Baseball Almanac, stores it in a SQLite database, and visualizes it through an interactive dashboard built with Streamlit.

├── scrape/ # Web scraper using Selenium
├── import/ # CSV-to-database script
├── output/ # Contains generated CSV files
├── mlb_stats.db # Final SQLite database
├── query_db.py # Command-line SQL query tool
├── dashboard.py # Streamlit dashboard app
├── README.md



# Web Scraping
    •	Opens Chrome in headless mode (no GUI).
	•	Pretends to be a real browser using a fake user-agent.
	•	Loops over each year (e.g. 2008, 2009).
	•	Opens the MLB yearly stats page on Baseball Almanac.
	•	Finds every table on the page.
	•	Tries to get the heading (h2/h3) just above each table.
	•	Cleans that heading and uses it to name a CSV file.
	•	Extracts data from each row of the table.
	•	Saves the data to a CSV in an output folder.
	•	Skips tables with no content.

# Data Cleaning & Transformation    

    This program reads a bunch of CSV files (baseball data), and puts each file into a separate table in a SQLite database called mlb_stats.db.

1. It goes into a folder named output and looks for all .csv files.
2. It opens each file and tries to:
	•	 Find the header (column names) — looks for a row starting with "Statistic"
	•	 Read the rest of the rows (the data)
3.For each column name:
	•	Removes weird characters
	•	Replaces spaces with underscores→ so that it works in SQL
It also figures out:
	•	Is each column a number? A decimal? Just text?→ It chooses the best data type for each column.
It also adds an extra column called year, based on the filename (like 2008_03_Hits.csv → year = 2008).
4. It gives each table a name like:
	•	table_1, table_2, table_3, etc.
Then it builds that table in the database with the correct columns and data types.
5. Each row from the CSV file is inserted into the matching table in the database, along with the year.
6. It moves to the next CSV file and does it all over again.
In the end, you’ll have a .db file with multiple tables — one for each CSV — that you can use for queries, dashboards, or analysis.

# Database Query Program

1. 	•	You're using the sqlite3 module to connect to the database.
	•	The database file is named mlb_stats.db.
2. It starts an infinite loop that prompts the user to type any SQL query.
   If the user types 'exit' or 'quit', it ends the loop.
3 The code executes the user's SQL query.
  It fetches the results (rows) and the column names to display.
4. it prints the column headers.
   Then it prints each row with clean formatting (tab-separated).
5. If the user types an invalid SQL query, it prints a helpful error message instead of crashing.

#  Dashboard Program

1.Imports Necessary Libraries

2. Shows a big title at the top of the page.

3.	•	Connects to the SQLite database.
	•	Loads data from table_1 into a DataFrame.
	•	@st.cache_data means: don’t reload unless data changes.
4. Strips spaces from column names (just in case).

5. Shows the first few rows of the dataset so users know what kind of data they’re working with.

6.User picks a year from the available list.

7. User picks a type of statistic (like "Runs", "Hits", etc.).

8.Filters the data to only show rows that match the selected year and statistic.

3 Visualizations

Bar Chart of Players
Histogram of the Statistic
Pie Chart of Teams

## Setup Instructions

1. **Clone this repo:**
   ```bash
   git clone https://github.com/faridahyderi/PythonFinalProject.git
   cd mlb-dashboard-project

2. Install dependencies
      pip install streamlit
      pip install pandas
      pip install matplotlib
      pip install selenium
      pip install -U webdriver-manager

3. Run the scraper:
    python3 scrape/mlb_scraper.py

4. Import CSVs into SQLite DB:
    python3 import/import_csv_to_db.py

5. Run the dashboard:
    streamlit run dashboard.py

