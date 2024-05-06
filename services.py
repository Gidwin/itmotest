from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Capital


async def is_city_table_empty(db_session: AsyncSession):
    query = select(Capital.id.isnot(None))
    query = select(exists(query))
    result = await db_session.execute(query)
    table_exists = result.scalars().one()

    return not (table_exists)
