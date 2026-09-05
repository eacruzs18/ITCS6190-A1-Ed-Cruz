import os, sys, time, json

import psycopg

# Environment variables with defaults
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = ...   # TODO: read DB_USER from the environment, defaulting to "appuser"
DB_PASS = ...   # TODO: read DB_PASS from the environment, defaulting to "secretpw"
DB_NAME = ...   # TODO: read DB_NAME from the environment, defaulting to "appdb"
TOP_N = int(os.getenv("APP_TOP_N", "5"))


def connect_with_retry(retries=10, delay=2):
    last_err = None
    for _ in range(retries):
        try:
            conn = psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                dbname=DB_NAME,
                connect_timeout=3,
            )
            return conn
        except Exception as e:
            last_err = e
            print("Waiting for database...", file=sys.stderr)
            time.sleep(delay)
    print("Failed to connect to Postgres:", last_err, file=sys.stderr)
    sys.exit(1)


def main():
    conn = connect_with_retry()
    with conn, conn.cursor() as cur:
        # Total number of trips
        # TODO: write a query that counts the rows in trips
        cur.execute("...")
        total_trips = cur.fetchone()[0]

        # Average fare by city
        # TODO: return one row per city with the average fare, rounded to 2 decimals,
        #       ordered by city. Name the second column avg_fare.
        cur.execute("""
            ...
        """)
        by_city = [{"city": c, "avg_fare": float(a)} for (c, a) in cur.fetchall()]

        # Top N trips by duration
        # TODO: return the TOP_N longest trips (city, minutes, fare), longest first.
        #       Break ties by city ascending. Use %s for the limit so it stays a
        #       parameter rather than string formatting.
        cur.execute("""
            ...
        """, (TOP_N,))
        # TODO: build a list of dicts with keys city, minutes and fare
        top = ...

        summary = {
            "total_trips": int(total_trips),
            "avg_fare_by_city": by_city,
            "top_by_minutes": top,
        }

        # Write to /out/summary.json
        os.makedirs("/out", exist_ok=True)
        with open("/out/summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        # Print to stdout
        print("=== Summary ===")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
