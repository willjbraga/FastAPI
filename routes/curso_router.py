from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from typing import Dict, List, Optional, Any
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends
from time import sleep

from routes import curso_router
from routes import usuario_router

from fastapi import Response

from models import Curso
from models import cursos



router = APIRouter()


def fake_db():
    try:
        print("Abrindo conexão com banco de dados")
        sleep(1)
    finally:
        print("Fechando conexão com banco de dados")
        sleep(1)



@router.get('/api/v1/cursos')
async def get_cursos():
    return {"info": "Todos os cursos"}


@router.get('/api/v1/cursos', 
         description='Retorna todos os cursos ou uma lista vazia.', 
         summary='Retorna todos os cursos', 
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso'
)
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

# todo input de usuário tipo o curso_id é por natureza uma string que precisa ser convertida em int (curso_id: int) -> type hint
@router.get('/api/v1/cursos/{curso_id}')
async def get_cursos(curso_id: int = Path(title="ID do Curso", description="Deve ser entre 1 e 2", gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')

# @app.post('/cursos', status_code=status.HTTP_201_CREATED)
# async def post_curso(curso: Curso):
#     if curso.id not in cursos:
#         cursos[curso.id] = curso
#         return curso
#     else:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Já existe um curso com ID {curso.id}")
    

@router.post('/api/v1/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso

@router.put('/api/v1/cursos/{curso_id}')
async def put_cursos(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Não existe um curso com id {curso_id}")

@router.delete('/api/v1/cursos/{curso_id}')
async def delete_cursos(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Não existe um curso com id {curso_id}")


#Esse exemplo usa 100% query parameters, segue o exemplo de requisição: http://localhost:8000/calculadora?a=10&b=10&c=10         
@router.get('/api/v1/calculadora')
async def calcular(a:int = Query(default=None, gt=5), b:int = Query(default=None, gt=10), c: Optional[int] = None, x_geek: str = Header(default=None)):
    soma = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {[x_geek]}')

    return {"resultado": soma}