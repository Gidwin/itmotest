from typing import Any, Dict, List

from pydantic import BaseModel, validator


class GeoLocation(BaseModel):
    type: str
    coordinates: List[float]

    @validator("type")
    def check_geojson(cls, value):
        if value != "Point":
            raise ValueError("geometry must have type 'Point'")
        return value

class GeoJSONFeature(BaseModel):
    type: str
    properties: Dict[str, Any]
    geometry: GeoLocation

    @validator("type")
    def check_geojson(cls, value):
        if value != "Feature":
            raise ValueError("geolocation must have type 'Feature'")
        return value


# class CapitalCreate(BaseModel):
#     geo_location: GeoJSONFeature

#     @validator("geo_location")
#     def check_geojson(cls, value):
#         if value.type != "Feature":
#             raise ValueError("geo_location must have type 'Feature'")
#         if value.geometry.type != "Point":
#             raise ValueError("geometry must have type 'Point'")
#         return value


# class CapitalPatch(BaseModel):
#     geo_location: GeoJSONFeature

#     @validator("geo_location")
#     def check_geojson(cls, value):
#         if value.type != "Feature":
#             raise ValueError("geo_location must have type 'Feature'")
#         if value.geometry.type != "Point":
#             raise ValueError("geometry must have type 'Point'")
#         return value
