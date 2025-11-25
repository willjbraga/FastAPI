from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = sessionmaker(
    #autocommit = False, -> código legado pois por padrão o autocommit já é fals
    autoflush = False,
    expire_on_commit = False,
    class_ = AsyncSession,
    bind = engine
)

#: AsyncSession