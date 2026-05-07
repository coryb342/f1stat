from sqlalchemy import select
from seeders.seeder import *
from models.session import Session
from models.session_circuit import Session_Circuit
from models.qualifying_result import Qualifying_Result
from models.race_result import Race_Result

def seed_sessions_and_results():
    db = establish_connection()
    years = ["2023", "2024", "2025"]

    for year in years:
        session_data = get_json_response(BASE_URL + "/" + year + "/races")
        race_sessions = session_data["MRData"]["RaceTable"]["Races"]

        for r in race_sessions:
            circuit = r["Circuit"]["circuitName"]
            quali_session = r["Qualifying"]
            q_session_id = year + r["round"] + "0"
            q_session_date = quali_session["date"]
            q_session_type = "Q"

            stmt = select(Session).where(Session.session_type == q_session_type).where(Session.session_date == q_session_date)
            existing_session = db.execute(stmt).scalar_one_or_none()

            if existing_session is None:
                session = Session(
                    session_id=q_session_id,
                    session_type=q_session_type,
                    session_date=q_session_date,
                    season=year
                    
                )
                db.add(session)
                db.commit()

            stmt = select(Session_Circuit).where(Session_Circuit.session_id == q_session_id).where(Session_Circuit.circuit_name == circuit)
            existing_session_circuit = db.execute(stmt).scalar_one_or_none()

            if existing_session_circuit is None:
                session_circuit = Session_Circuit(
                    session_id=q_session_id,
                    circuit_name=circuit
                )
                db.add(session_circuit)
                db.commit()
            
            quali_result_data = get_json_response(BASE_URL + "/" + year + "/" + r["round"] + "/qualifying")
            quali_results = quali_result_data["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]

            for qr in quali_results:
                stmt = select(Qualifying_Result).where(Qualifying_Result.session_id == q_session_id).where(Qualifying_Result.driver_code == qr["Driver"]["code"])
                existing_qr = db.execute(stmt).scalar_one_or_none()

                if existing_qr is None:
                    qualifying_result = Qualifying_Result(
                        session_id=q_session_id,
                        driver_code=qr["Driver"]["code"],
                        position=qr["position"],
                        Q1_time=qr.get("Q1", ""),
                        Q2_time=qr.get("Q2", ""),
                        Q3_time=qr.get("Q3", "")
                    )
                    db.add(qualifying_result)
                    db.commit()
            
            r_session_id = year + r["round"] + "1"
            r_session_date = r["date"]
            race_result_data = get_json_response(BASE_URL + "/" + year + "/" + r["round"] + "/results")
            race_results = race_result_data["MRData"]["RaceTable"]["Races"][0]["Results"]
            r_session_type = "R"

            stmt = select(Session).where(Session.session_type == r_session_type).where(Session.session_date == r_session_date)
            existing_session = db.execute(stmt).scalar_one_or_none()

            if existing_session is None:
                session = Session(
                    session_id=r_session_id,
                    session_type=r_session_type,
                    session_date=r_session_date,
                    season=year
                )
                db.add(session)
                db.commit()

            stmt = select(Session_Circuit).where(Session_Circuit.session_id == r_session_id).where(Session_Circuit.circuit_name == circuit)
            existing_session_circuit = db.execute(stmt).scalar_one_or_none()

            if existing_session_circuit is None:
                session_circuit = Session_Circuit(
                    session_id=r_session_id,
                    circuit_name=circuit
                )
                db.add(session_circuit)
                db.commit()
            
            for rr in race_results:
                stmt = select(Race_Result).where(Race_Result.session_id == r_session_id).where(Race_Result.driver_code == rr["Driver"]["code"])
                existing_rr = db.execute(stmt).scalar_one_or_none()

                if existing_rr is None:
                    fastest_lap = rr.get("FastestLap", "")
                    race_result = Race_Result(
                        session_id=r_session_id,
                        driver_code=rr["Driver"]["code"],
                        position=rr["position"],
                        points_earned=rr["points"],
                        fastest_lap_time=rr["FastestLap"]["Time"]["time"] if fastest_lap != "" else "NA"
                    )
                    db.add(race_result)
                    db.commit() 