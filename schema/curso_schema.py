from typing import Optional
from pydantic import BaseModel as SCBaseModel, ConfigDict

class CursoSchema(SCBaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    # substitui o antigo Config.orm_mode = True
    model_config = ConfigDict(from_attributes=True)
