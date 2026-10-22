from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

meus_livros = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int


@app.get("/Livros")
def get_livros():
    if not meus_livros:
        return {"message": "Não existe nenhum livro"}
    else:
        return {"Livros": meus_livros}


@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Esse livro ja existe")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "O livro foi adicionado com sucesso"}


@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse não existe")
    else:
        meus_livros[id_livro] = livro.model_dump()

        return {"message": "O livro foi atualizado"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado")
    else:
        del meus_livros[id_livro]

        return {"message": "Seu livro foi deletado"}
