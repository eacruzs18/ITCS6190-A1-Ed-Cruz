# Assignment #1: Containers with Docker

> This project runs a Postgres database and a Python script together inside Docker. 
> Once the database starts up, the Python script connects to it, calculates trip stats 
> like averages and top durations, and saves the results as a JSON file.
>
> **Name: Ed Cruz**
> **Student ID: 801337361**
> **Email: ecruz13@charlotte.edu**

A two-container stack: a PostgreSQL database seeded from `db/init.sql`, and a Python app
that queries it, computes a few statistics, prints them, and writes `out/summary.json`.


## Repository layout

```
.
├─ app/           main.py, Dockerfile
├─ db/            init.sql, Dockerfile
├─ out/           summary.json (created at run time)
├─ compose.yml
├─ Makefile
├─ .gitignore
└─ README.md
```

## How to run

```bash
make            # clean, build, and start both services
make down       # stop and remove the containers and volumes
```

Or without make:

```bash
docker compose up --build
```

The app connects to the database, runs its queries, prints a JSON summary to the terminal
and writes the same summary to `out/summary.json`.

## Output

```json
{
  "total_trips": 6,
  "avg_fare_by_city": [
    {
      "city": "Charlotte",
      "avg_fare": 16.25
    },
    {
      "city": "New York",
      "avg_fare": 19.0
    },
    {
      "city": "San Francisco",
      "avg_fare": 20.25
    }
  ],
  "top_by_minutes": [
    {
      "city": "San Francisco",
      "minutes": 28,
      "fare": 29.3
    },
    {
      "city": "New York",
      "minutes": 26,
      "fare": 27.1
    },
    {
      "city": "Charlotte",
      "minutes": 21,
      "fare": 20.0
    },
    {
      "city": "Charlotte",
      "minutes": 12,
      "fare": 12.5
    },
    {
      "city": "San Francisco",
      "minutes": 11,
      "fare": 11.2
    },
    {
      "city": "New York",
      "minutes": 9,
      "fare": 10.9
    }
  ]
}
```

## Where outputs are written

`out/summary.json`, which is bind-mounted from the `app` container's `/out`.

## Troubleshooting

- **The app exits before the database is ready.** `compose.yml` already waits on the db
  healthcheck, and `main.py` retries. If it still fails, check the credentials match
  between the two services.
- **Permission errors on `out/`.** On Linux the bind-mounted directory may end up owned by
  root. `sudo chown -R $USER out` fixes it; `make clean` recreates the directory.
- **Stale database.** The seed script in `db/init.sql` runs only on first initialisation.
  Run `make down` (which passes `-v` and drops the volume) before starting again.

## Notes on credentials

The database user and password here are throwaway values used only on your machine, so
committing them is fine for this assignment. Real credentials belong in a `.env` file that
is listed in `.gitignore`.
