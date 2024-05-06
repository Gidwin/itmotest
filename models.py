from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Capital(Base):
    __tablename__ = "capital"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326)
    )
