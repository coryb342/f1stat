import os
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session as DBSession
from dotenv import load_dotenv
from models.circuit import Circuit
from models.driver import Driver
from models.qualifying_result import Qualifying_Result
from models.race_result import Race_Result
from models.session_circuit import Session_Circuit
from models.session import Session
from models.user import User
from models.constructor import Constructor


load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
def establish_connection():
    try:
        engine = create_engine(DB_URL)
        session = DBSession(engine)
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return

    return session

def findUser(self, email):
    stmt = select(User).where(User.email == email)
    user = self.app.db.execute(stmt).scalars().first()

    if not user:
        return None

    return user

def findUsersFavoriteDriver(self, user):
    favorite_driver_stmt = select(Driver).where(Driver.driver_code == user.favorite_driver)
    favorite_driver = self.app.db.execute(favorite_driver_stmt).scalars().first()

    return favorite_driver

def fetchAllDrivers(self):
    driver_stmt = select(Driver).order_by(Driver.last_name)
    drivers = self.app.db.execute(driver_stmt).scalars().all()

    return drivers

def fetchAllCircuits(self):
    circuit_stmt = select(Circuit).order_by(Circuit.circuit_name)
    circuits = self.app.db.execute(circuit_stmt).scalars().all()

    return circuits

def createUser(self, user_data):
    new_user = User(
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            favorite_driver=user_data.get('favorite_driver'),
            password=user_data.get('password')
        )

    self.app.db.add(new_user)
    self.app.db.commit()

def fetchStats(self):
        pole_results = {}
        wins_results = {}
        fastest_lap_results = {}
        points_results = {}
        podiums_results = {}

        pole_stmt = (
            select(Qualifying_Result.driver_code, func.count(Qualifying_Result.position).label("pole_positions"))
            .join(Session, Qualifying_Result.session_id == Session.session_id)
            .where(Qualifying_Result.driver_code.in_(self.drivers_selected))
            .where(Qualifying_Result.position == 1)
            .where(Session.season.in_(self.seasons_selected))
            .group_by(Qualifying_Result.driver_code)
        ) 
        wins_stmt = (
            select(Race_Result.driver_code, func.count(Race_Result.position).label("wins"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers_selected))
            .where(Race_Result.position == 1)
            .where(Session.season.in_(self.seasons_selected))
            .group_by(Race_Result.driver_code)
        )
        fastest_lap_stmt = (
            select(Race_Result.driver_code, func.min(Race_Result.fastest_lap_time).label("fastest_lap"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers_selected))
            .where(Race_Result.fastest_lap_time != "NA")
            .where(Session.season.in_(self.seasons_selected))
            .group_by(Race_Result.driver_code)
        )
        points_stmt = (
            select(Race_Result.driver_code, func.sum(Race_Result.points_earned).label("total_points"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers_selected))
            .where(Session.season.in_(self.seasons_selected))
            .group_by(Race_Result.driver_code)
        )
        podiums_stmt = (
            select(Race_Result.driver_code, func.count(Race_Result.position).label("podiums"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers_selected))
            .where(Race_Result.position <= 3)
            .where(Session.season.in_(self.seasons_selected))
            .group_by(Race_Result.driver_code)
        )

        if "pole_positions" in self.stats_selected:
            pole_results = {r.driver_code: r.pole_positions for r in self.app.db.execute(pole_stmt).all()}
        if "wins" in self.stats_selected:
            wins_results = {r.driver_code: r.wins for r in self.app.db.execute(wins_stmt).all()}
        if "points" in self.stats_selected:
            points_results = {r.driver_code: r.total_points for r in self.app.db.execute(points_stmt).all()}
        if "fastest_lap" in self.stats_selected:
            fastest_lap_results = {r.driver_code: r.fastest_lap for r in self.app.db.execute(fastest_lap_stmt).all()}
        if "podiums" in self.stats_selected:
            podiums_results = {r.driver_code: r.podiums for r in self.app.db.execute(podiums_stmt).all()}

        return pole_results, wins_results, fastest_lap_results, points_results, podiums_results

def fetchRaceResults(self):
    race_results_stmt = (
        select(
            Session.session_date,
            Race_Result.driver_code,
            Driver.first_name,
            Driver.last_name,
            Session_Circuit.circuit_name,
            Race_Result.position,
            Race_Result.points_earned,
            Race_Result.fastest_lap_time
        )
        .select_from(Race_Result)
        .join(Session, Race_Result.session_id == Session.session_id)
        .join(Session_Circuit, Race_Result.session_id == Session_Circuit.session_id)
        .join(Driver, Race_Result.driver_code == Driver.driver_code)
        .where(Session.season.in_(self.seasons_selected))
        .where(Race_Result.driver_code.in_(self.drivers_selected))
        .where(Session_Circuit.circuit_name.in_(self.circuits_selected))
        .order_by(Session.session_date)
        .order_by(Race_Result.position)
    )

    return self.app.db.execute(race_results_stmt).all()

def fetchQualifyingResults(self):
    quali_results_stmt = (
        select(
            Session.session_date,
            Qualifying_Result.driver_code,
            Driver.first_name,
            Driver.last_name,
            Session_Circuit.circuit_name,
            Qualifying_Result.position,
            Qualifying_Result.Q1_time,
            Qualifying_Result.Q2_time,
            Qualifying_Result.Q3_time
        )
        .select_from(Qualifying_Result)
        .join(Session, Qualifying_Result.session_id == Session.session_id)
        .join(Session_Circuit, Qualifying_Result.session_id == Session_Circuit.session_id)
        .join(Driver, Qualifying_Result.driver_code == Driver.driver_code)
        .where(Session.season.in_(self.seasons_selected))
        .where(Qualifying_Result.driver_code.in_(self.drivers_selected))
        .where(Session_Circuit.circuit_name.in_(self.circuits_selected))
        .order_by(Session.session_date)
        .order_by(Qualifying_Result.position)
    )

    return self.app.db.execute(quali_results_stmt).all()

def findDriverByCode(self, driver_code):
    find_driver_stmt = select(Driver).where(Driver.driver_code == driver_code)
    driver = self.app.db.execute(find_driver_stmt).scalars().first()

    return driver


