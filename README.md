## About
F1Stats is a simple application that allows you to view driver stats, race results and qualifying results from the 2023, 2024, and 2025 seasons.

User interface built using Textual: https://textual.textualize.io/

All data used to seed the database is aquired through the use of the jolpica-f1 API: https://github.com/jolpica/jolpica-f1.

**Author**: Cory Bateman

**Date Last Updated**: 05/13/2026

## Getting Started
### Requirements
- Python3
- PostgreSQL
  
### Packages
- `pip install sqlalchemy psycopg2-binary python-dotenv textual textual-dev rich bcrypt requests`

### Building and Seeding the Database
1. Create an empty db in postgres
   - `createdb <dbname>`
2. Copy the .env.example as .env file and add your db parameters. You will need:
   - DB_NAME
   - DB_USERNAME
   - DB_PASSWORD
   - DB_HOST
   - DB_PORT
3. To Build and Seed the Database Run the following command from the project root:
   - `python3 db_builder.py --seed`
     
   This will seed the database with data from the 2023, 2024, and 2025 seasons. Working on a feature to be able to select the years to seed with.

   **Note: If you need to rebuild and not re-seed, just drop the --seed. (Useful if future tables are added)**

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
1. From the main menu select Session Results
2. Select Session Type (Race or Quali)
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
3. Next, select the Driver(s).
4. Then, select the Circuit(s):
5. Finally, select season year(s):
6. Hit Fetch Results

### Getting Driver Stats
1. From the main menu select Driver Stats.
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
5. Hit Fetch Stats

**NOTE: Although the pages are mostly scrollable within the terminal, sometimes you may need to extend the terminal to see everything.**

## Screenshots

<img width="883" height="681" alt="f1statlogin" src="https://github.com/user-attachments/assets/e864edd1-37e6-4c08-9ec8-2192c31e6194" />
<img width="883" height="681" alt="f1stathome" src="https://github.com/user-attachments/assets/5c3dc572-8c54-4720-8d48-e1a357a8e410" />
<img width="883" height="757" alt="f1statdriverselect" src="https://github.com/user-attachments/assets/dd0b894a-6361-4c3a-94e1-8b48225b86f8" />
<img width="883" height="757" alt="f1statdriverstatselect" src="https://github.com/user-attachments/assets/0c0b6952-bef1-4087-8b94-7a67b09d1d70" />
<img width="883" height="757" alt="f1statdriverstattable" src="https://github.com/user-attachments/assets/7d0cb800-5041-4433-b6cd-3479624d0df6" />
https://github.com/user-attachments/assets/8c61f549-8d3b-4e20-a56b-9058a9808801




