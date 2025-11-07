from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from typing import List, Optional
from fastapi import Path
from fastapi import Query
from fastapi import Header

from fastapi import Response

from models import Curso

app = FastAPI()

cursos = {
    1:{
        "titulo": "Programação para Leigos",
        "aulas": 112,
        "horas": 58
    },
    2:{
        "titulo": "Algoritmos e Lógica de Programação",
        "aulas": 87,
        "horas": 67
    }
}

@app.get('/cursos')
async def get_cursos():
    return cursos

# todo input de usuário tipo o curso_id é por natureza uma string que precisa ser convertida em int (curso_id: int) -> type hint
@app.get('/cursos/{curso_id}')
async def get_cursos(curso_id: int = Path(title="ID do Curso", description="Deve ser entre 1 e 2", gt=0, lt=3)):
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
    

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso

@app.put('/cursos/{curso_id}')
async def put_cursos(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Não existe um curso com id {curso_id}")

@app.delete('/cursos/{curso_id}')
async def delete_cursos(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Não existe um curso com id {curso_id}")


#Esse exemplo usa 100% query parameters, segue o exemplo de requisição: http://localhost:8000/calculadora?a=10&b=10&c=10         
@app.get('/calculadora')
async def calcular(a:int = Query(default=None, gt=5), b:int = Query(default=None, gt=10), c: Optional[int] = None, x_geek: str = Header(default=None)):
    soma = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {[x_geek]}')

    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)