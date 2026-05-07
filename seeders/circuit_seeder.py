from sqlalchemy import select
from seeders.seeder import *
from models.circuit import Circuit

def seed_circuits():
    db = establish_connection()
    years = ["2023", "2024", "2025"]

    for year in years:
        
        circuits_data = get_json_response(BASE_URL + "/" + year + "/circuits")
        circuits = circuits_data["MRData"]["CircuitTable"]["Circuits"]

        for c in circuits:
            circuit_name = c["circuitName"]
            location = c["Location"]["locality"]
            country = c["Location"]["country"]

            stmt = select(Circuit).where(Circuit.circuit_name == circuit_name)
            existing_circuit = db.execute(stmt).scalar_one_or_none()

            if existing_circuit is not None:
                continue

            else:
                circuit = Circuit(
                    circuit_name=circuit_name,
                    location=location,
                    country=country
                )
                db.add(circuit)
                db.commit()