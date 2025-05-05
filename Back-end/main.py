from fastapi import FastAPI
from database import Base, engine
from routes import auth

# Cria as tabelas no banco de dados (se ainda não existirem)
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI()

# Inclui as rotas do arquivo auth.py com prefixo /auth
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Roda o servidor se o arquivo for executado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
