import csv

from fastapi import Depends, FastAPI, HTTPException
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import Capital
from schema import GeoJSONFeature
from services import is_city_table_empty

app = FastAPI()


@app.get("/load-data")
async def load_cities(db_session: AsyncSession = Depends(get_async_session)):
    if await is_city_table_empty(db_session):
        cities = []
        with open("capitals.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)
            for row in csv_reader:
                city = Capital(
                    country=row[1],
                    city=row[2],
                    geo_location=f"POINT({row[3]} {row[4]})",
                )
                cities.append(city)
            db_session.add_all(cities)
            await db_session.commit()
            return {"message": "Data loaded successfully"}
    return {"message": "Data is already loaded"}


@app.get("/capitals")
async def get_capitals(db_session: AsyncSession = Depends(get_async_session)):
    capitals = await db_session.execute(select(Capital))
    capitals = capitals.scalars().all()
    geojson_capitals = []
    for capital in capitals:
        geojson_capital = {
            "type": "Feature",
            "properties": {"country": capital.country,
                           "city": capital.city},
            "geometry": mapping(to_shape(capital.geo_location)),
        }
        geojson_capitals.append(geojson_capital)
    return {"type": "FeatureCollection", "features": geojson_capitals}


@app.get("/capitals/{capital_id}")
async def get_capitals(
    capital_id: int, db_session: AsyncSession = Depends(get_async_session)
):
    capital_query = select(Capital).where(Capital.id == capital_id)
    capital = await db_session.execute(capital_query)
    data = capital.scalar()
    geojson_capital = {
        "type": "Feature",
        "properties": {"country": data.country,
                       "city": data.city},
        "geometry": mapping(to_shape(data.geo_location)),
    }
    return geojson_capital


@app.post("/capitals", status_code=201)
async def create_capital(
    capital_data: GeoJSONFeature, db_session: AsyncSession = Depends(get_async_session)
):
    coordinates = capital_data.geometry.coordinates
    country = capital_data.properties['country']
    city = capital_data.properties['city']
    new_capital = Capital(
        country=country,
        city=city,
        geo_location=f"POINT({coordinates[0]} {coordinates[1]})",
    )
    db_session.add(new_capital)
    await db_session.commit()
    return {"message": "create new obj"}


@app.patch("/capitals/{capital_id}", status_code=200)
async def update_capital(
    capital_id: int,
    capital_data: GeoJSONFeature,
    db_session: AsyncSession = Depends(get_async_session),
):
    capital = await db_session.get(Capital, capital_id)
    if capital:
        coordinates = capital_data.geometry.coordinates
        capital.city = capital_data.properties['city']
        capital.geo_location = f"POINT({coordinates[0]} {coordinates[1]})"
        await db_session.commit()
        return {"message": "change complite"}
    else:
        raise HTTPException(status_code=404, detail="Capital not found")


@app.delete("/capitals/{capital_id}", status_code=204)
async def delete_capital(
    capital_id: int, db_session: AsyncSession = Depends(get_async_session)
):
    capital = await db_session.get(Capital, capital_id)
    if capital:
        await db_session.delete(capital)
        await db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="Capital not found")
