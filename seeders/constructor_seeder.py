from sqlalchemy import select
from seeders.seeder import *
from models.constructor import Constructor

def seed_constructors():
    db = establish_connection()
    years = ["2023", "2024", "2025"]

    for year in years:
        
        constructors_data = get_json_response(BASE_URL + "/" + year + "/constructors")
        constructors = constructors_data["MRData"]["ConstructorTable"]["Constructors"]

        for c in constructors:
            constructor_name = c["name"]
            constructor_nationality = c["nationality"]

            stmt = select(Constructor).where(Constructor.name == constructor_name)
            existing_constructor = db.execute(stmt).scalar_one_or_none()

            if existing_constructor is not None:
                continue

            else:
                constructor = Constructor(
                    name=constructor_name,
                    nationality=c["nationality"]
                )
                db.add(constructor)
                db.commit() 
