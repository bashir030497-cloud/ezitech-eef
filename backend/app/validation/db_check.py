import os


DB_INDICATORS = ["models", "migrations", "schema.sql", "database.py", "prisma"]


def check_database(local_path: str) -> dict:
    found = []
    for root, dirs, files in os.walk(local_path):
        for indicator in DB_INDICATORS:
            if indicator in dirs or indicator in files:
                found.append(indicator)

    return {
        "db_indicators_found": found,
        "passed": len(found) > 0,
    }
