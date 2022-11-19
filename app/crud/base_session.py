from sqlalchemy.ext.asyncio import AsyncSession


class BaseSession:
     def __init__(self, session: AsyncSession):
          self.session = session
          
