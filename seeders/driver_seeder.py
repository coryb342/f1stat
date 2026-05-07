from sqlalchemy import select
from seeders.seeder import *
from models.driver import Driver

def seed_drivers():
    db = establish_connection()
    years = ["2023", "2024", "2025"]

    for year in years:
        drivers_data = get_json_response(BASE_URL + "/" + year + "/drivers")
        drivers = drivers_data["MRData"]["DriverTable"]["Drivers"]

        for d in drivers:
            driver_code = d.get("code", "")

            if driver_code == "":
                continue
            
            stmt = select(Driver).where(Driver.driver_code == driver_code)
            existing_driver = db.execute(stmt).scalar_one_or_none()

            if existing_driver is not None:
                continue

            else:
                driver = Driver(
                    driver_code=driver_code,
                    first_name=d["givenName"],
                    last_name=d["familyName"],
                    nationality=d["nationality"]
                )
                db.add(driver)
                db.commit()
