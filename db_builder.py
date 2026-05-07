from db import *
import models
from seeders.constructor_seeder import seed_constructors
from seeders.circuit_seeder import seed_circuits
from seeders.driver_seeder import seed_drivers
from seeders.session_and_results_seeder import seed_sessions_and_results
import argparse

def build_db(seed=False):
    try:
        print(Base.metadata.tables.keys())
        engine = create_engine(DB_URL)
        Base.metadata.create_all(engine)
        print("Database built successfully.")
    except Exception as e:
        print(f"An error occurred while building the database: {e}")
        return
    
    if not seed:
        return
    
    try:
        seed_drivers()
        print("Drivers seeded successfully.")
        seed_constructors()
        print("Constructors seeded successfully.")
        seed_circuits()
        print("Circuits seeded successfully.")
        seed_sessions_and_results()
        print("Sessions and results seeded successfully.")
        print("All seeders completed successfully.")
    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
        return
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="store_true", help="Seed the database with initial data")
    args = parser.parse_args()
    build_db(seed=args.seed)

