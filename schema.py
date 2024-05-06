from typing import List, Any, Dict
from pydantic import BaseModel, validator

class GeoLocation(BaseModel):
    type: str
    coordinates: List[float]

class GeoJSONFeature(BaseModel):
    type: str
    properties: Dict[str, Any]
    geometry: GeoLocation

class CapitalCreate(BaseModel):
    country: str
    city: str
    geo_location: GeoJSONFeature

    @validator("geo_location")
    def check_geojson(cls, value):
        if value.type != "Feature":
            raise ValueError("geo_location must have type 'Feature'")
        if value.geometry.type != "Point":
            raise ValueError("geometry must have type 'Point'")
        return value
    
class CapitalPatch(BaseModel):
    city: str
    geo_location: GeoJSONFeature

    @validator("geo_location")
    def check_geojson(cls, value):
        if value.type != "Feature":
            raise ValueError("geo_location must have type 'Feature'")
        if value.geometry.type != "Point":
            raise ValueError("geometry must have type 'Point'")
        return value