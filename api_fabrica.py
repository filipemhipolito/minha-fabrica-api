import json
import os
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

# Inicializa a API
app = FastAPI(title="Fábrica de IA API")
FICHEIRO_ARMAZEM = "armazem_logistica.json"

def ler_armazem():
    """Lê o armazém de ferramentas gerado pela Fábrica."""
    if not os.path.exists(FICHEIRO_ARMAZEM):
        return {}
    with open(FICHEIRO_ARMAZEM, "r") as f:
        data = json.load(f)
        return data.get("ferramentas_a_venda", {})

@app.get("/listar-ferramentas")
def listar_ferramentas():
    """Mostra aos clientes que ferramentas temos em stock."""
    return {"stock_atual": list(ler_armazem().keys())}

@app.post("/executar")
def executar_servico(payload: dict = Body(...)):
    """
    O endpoint principal onde os clientes enviam o ID da ferramenta 
    e os argumentos para a execução.
    """
    ferramenta_id = payload.get("ferramenta_id")
    argumentos = payload.get("argumentos")
    
    stock = ler_armazem()
    
    if ferramenta_id not in stock:
        raise HTTPException(status_code=404, detail="Ferramenta não encontrada no armazém.")
    
    # Extrair o código que a tua IA escreveu
    codigo = stock[ferramenta_id]["codigo"]
    
    try:
        # Cria um ambiente seguro para executar o código
        namespace = {}
        exec(codigo, namespace)
        
        # Chama a função 'executar' que o teu DEV criou
        resultado = namespace["executar"](**argumentos)
        
        # Incrementa as vitórias (opcional: podes criar um sistema de logs)
        return {
            "status": "sucesso",
            "resultado": resultado
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na execução da ferramenta: {str(e)}")