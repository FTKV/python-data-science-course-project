from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def add_custom_aggregate(session: AsyncSession):
    sql_query_1 = """
CREATE OR REPLACE FUNCTION first_or_none_agg(state anyelement, value anyelement)
RETURNS anyelement
AS $$
BEGIN
    IF state IS NULL THEN
        RETURN value;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;
"""
    sql_query_2 = """
CREATE AGGREGATE first_or_none(anyelement) (
    SFUNC = first_or_none_agg,
    STYPE = anyelement
);
"""
    await session.execute(text(sql_query_1))
    await session.execute(text(sql_query_2))
