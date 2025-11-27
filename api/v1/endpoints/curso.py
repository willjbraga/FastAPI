from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.curso_model import CursoModel
from schema.curso_schema import CursoSchema
from core.deps import get_session

router = APIRouter()

# POST curso
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, 
                            aulas=curso.aulas, 
                            horas=curso.horas)

    db.add(novo_curso)
    await db.commit()
    await db.refresh(novo_curso)

    return novo_curso

# GET cursos
@router.get('/', response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    query = select(CursoModel)
    result = await db.execute(query)
    cursos: List[CursoModel] = result.scalars().all()

    return cursos

# GET curso
@router.get('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    query = select(CursoModel).where(CursoModel.id == curso_id)
    result = await db.execute(query)
    curso = result.scalar_one_or_none()

    if curso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado."
        )

    return curso

# PUT curso
@router.put('/{curso_id}', response_model= CursoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    query = select(CursoModel).where(CursoModel.id == curso_id)
    result = await db.execute(query)
    curso_update = result.scalar_one_or_none()

    if curso_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado."
        )

    curso_update.titulo = curso.titulo
    curso_update.aulas = curso.aulas
    curso_update.horas = curso.horas

    await db.commit()
    await db.refresh(curso_update)

    return curso_update

# DELETE curso
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    query = select(CursoModel).where(CursoModel.id == curso_id)
    result = await db.execute(query)
    curso_delete = result.scalar_one_or_none()
    
    if curso_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado."
        )

    await db.delete(curso_delete)
    await db.commit()
    
    return None
