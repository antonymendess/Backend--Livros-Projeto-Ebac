import os
import secrets
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI(
    title="API de Livros",
    description="API para gerencias catálogo de livros",
    version="1.0.0",
    contact={"name":"Antony Mendes", "email":"antonymcypriano@gmail.com"}
)

security = HTTPBasic()


MEU_USUARIO = "admin"
MINHA_SENHA = "admin"


meus_livros = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int


def autenticar_meu_usuario(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    
    is_username_correct = secrets.compare_digest(
        credentials.username.encode("utf-8"), MEU_USUARIO.encode("utf-8")
    )
    is_password_correct = secrets.compare_digest(
        credentials.password.encode("utf-8"), MINHA_SENHA.encode("utf-8")
    )

    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username




@app.get("/Livros")
def get_livros(page: int = 1, limit: int = 10, usuario: str = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores invalidos")
    
    if not meus_livros:
        return {"message": "Não existe nenhum livro"}
    
    start = (page -1) * limit
    end = start + limit

    livros_paginados = [{"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
                        for id_livro, livro_data in list(meus_livros.items())[start:end]
    ]
    

    return {
        "page": page,
        "limit": limit,
        "total": len(meus_livros),
        "livros": livros_paginados
    }


@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, usuario: str = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Esse livro ja existe")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "O livro foi adicionado com sucesso"}


@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro, usuario: str = Depends(autenticar_meu_usuario)):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse não existe")
    else:
        meus_livros[id_livro] = livro.model_dump()

        return {"message": "O livro foi atualizado"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int, usuario: str = Depends(autenticar_meu_usuario)):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado")
    else:
        del meus_livros[id_livro]

        return {"message": "Seu livro foi deletado"}
