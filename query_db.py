import sqlite3

DB_FILE = "mlb_stats.db"

def run_query():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Welcome to the MLB Stats Query Tool!")
    print("Type your SQL query or type 'exit' to quit.\n")

    while True:
        query = input("SQL> ").strip()
        if query.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            if columns:
                # Print column headers
                print("\t".join(columns))
                print("-" * (8 * len(columns)))

                # Print rows
                for row in rows:
                    print("\t".join(str(cell) for cell in row))
            else:
                print(f"Query executed successfully. Rows affected: {cursor.rowcount}")

        except sqlite3.Error as e:
            print(f"SQL Error: {e}")

    conn.close()

if __name__ == "__main__":
    run_query()
