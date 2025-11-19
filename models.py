from typing import Optional
from pydantic import BaseModel, field_validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    #isso tudo é feito pelo pydantic
    #para cada campo ou atributo deve ter um if próprio
    @field_validator('titulo')
    def validar_titulo(cls, value):
        palavras = value.split()
        if len(palavras) < 3:
            raise ValueError('O titulo deve ter pelo menos 3 palavras')
        return value

cursos = [
    Curso(id=1, titulo='Programação para Leigos', aulas=42, horas=56),
    Curso(id=2, titulo='Algoritmos e Lógica de Programação', aulas=86, horas=67)
]


