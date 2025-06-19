import os
import sqlite3
import csv
import re

CSV_FOLDER = "output"
DB_FILE = "mlb_stats.db"

def infer_sql_type(value):
    try:
        int(value)
        return "INTEGER"
    except:
        try:
            float(value)
            return "REAL"
        except:
            return "TEXT"

def clean_column_name(name):
    # Remove all non-alphanumeric and underscore chars, replace spaces with underscores
    cleaned = re.sub(r'\W+', '_', name.strip())
    # Prevent empty column names
    return cleaned if cleaned else "col"

def quote_identifier(name):
    # Escape double quotes by doubling them, then wrap with double quotes
    escaped = name.replace('"', '""')
    return '"' + escaped + '"'

def import_csv_to_sqlite():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for filename in os.listdir(CSV_FOLDER):
        if filename.endswith(".csv"):
            filepath = os.path.join(CSV_FOLDER, filename)
            print(f"\n[+] Importing {filename}...")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    
                    # Skip initial non-header lines until you find a proper header row
                    for row in reader:
                        if row and row[0].strip() == "Statistic":  # detect header row
                            headers = [clean_column_name(h) for h in row]
                            break
                    else:
                        print(f" No valid header found in {filename}, skipping")
                        continue
                    
                    rows = []
                    for row in reader:
                        # Skip empty or malformed rows
                        if len(row) != len(headers):
                            # You can log this or just skip
                            continue
                        rows.append(row)

                    match = re.match(r"(\d{4})_(\d+)_.*\.csv", filename)
                    year = int(match.group(1)) if match else None
                    idx = int(match.group(2)) if match else 0

                    # MODIFY here: use year in table name to avoid overwrite
                    table_name = f"table_{year}_{idx}"

                    types = []
                    for i in range(len(headers)):
                        sample_value = next((r[i] for r in rows if r[i].strip()), "")
                        types.append(infer_sql_type(sample_value))

                    headers.append("year")
                    types.append("INTEGER")

                    cursor.execute(f'DROP TABLE IF EXISTS {quote_identifier(table_name)}')

                    columns_with_types = [
                        f"{quote_identifier(headers[i])} {types[i]}" for i in range(len(headers))
                    ]
                    create_stmt = f"CREATE TABLE {quote_identifier(table_name)} (" + ", ".join(columns_with_types) + ")"
                    cursor.execute(create_stmt)

                    placeholders = ", ".join(["?"] * len(headers))
                    insert_sql = f"INSERT INTO {quote_identifier(table_name)} VALUES ({placeholders})"

                    for row in rows:
                        row = row + [year]  # add year column
                        cursor.execute(insert_sql, row)

                    conn.commit()
                    print(f" Imported {len(rows)} rows into '{table_name}'")

            except Exception as e:
                print(f" Error importing {filename}: {e}")

    conn.close()
    print("\n All CSV files imported into mlb_stats.db")


if __name__ == "__main__":
    import_csv_to_sqlite()
