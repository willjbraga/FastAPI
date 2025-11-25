from core.configs import settings
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class CursoModel(settings.DBBaseModel):
    __tablename__= 'cursos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement= True)
    titulo: Mapped[str] = mapped_column(String(100))
    aulas: Mapped[int] = mapped_column(Integer)
    horas: Mapped[int] = mapped_column(Integer) 