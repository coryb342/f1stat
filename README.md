## About
F1Stats is a simple application that allows you to view driver stats, race results and qualifying results from the 2023, 2024, and 2025 seasons.

All data used to seed the database is aquired through the use of the jolpica-f1 API.

**Author**: Cory Bateman

**Date Last Updated**: 05/04/2026

## Getting Started
### Requirements
- Python3
- PostgreSQL
  
## Packages
- `pip install sqlalchemy psycopg2-binary python-dotenv textual textual-dev rich bcrypt requests`

### Building and Seeding the Database
1. Create an empty db in postgres
   - `createdb <dbname>`
2. Update the .env file with your db parameters. You will need:
   - DB_NAME
   - DB_USERNAME
   - DB_PASSWORD
   - DB_HOST
   - DB_PORT
3. To Build and Seed the Database Run the following command from the project root:
   - `python3 db_builder.py --seed`
   Note: If you need to rebuild and not re-seed, just drop the --seed. (Useful if future tables are added)

### Running the Application
Simple as running `python3 main.py` from the project root.

## Application Flow
### Creating an Account
When the application launches you will be asked to either login or create an account.

If it is your first time you will want to create an account.

You will be asked to provide:
- Email
- First Name
- Last Name
- Password (Will be hashed don't worry)

You will then need to select your favorite driver from the list.

Once you have finished creating your account, you will arrive at the main screen.

### Seeing whats in the DB
- List all Circuits
- List all Drivers
### Getting Session Results
1. First Select Session Type (Race or Quali)
   - Race session provides:
     - Session Details
     - Driver Info
     - Circuit
     - Position
     - Points Earned
     - Fastest Lap Time (When Applicable)
   - Quali session provides:
     - Session Details
     - Driver Info
     - Circuit
     - Position
     - Q1 Time (When Applicaple)
     - Q2 Time (When Applicaple)
     - Q3 Time (When Applicable)
2. Next, select the Driver(s).
3. Then, select the Circuit(s):
4. Finally, select season year(s):
5. Hit Fetch Results

### Getting Driver Stats
1. From the main menu select See Driver Statistics.
2. Select driver(s) from the list and hit continue.
3. Choose stat(s):
   - Number of Pole Positions
   - Number of Wins
   - Total Points
   - Fastest Lap
4. Select Season Year(s):
   - 2023
   - 2024
   - 2025
5. Hit Fetch Results

