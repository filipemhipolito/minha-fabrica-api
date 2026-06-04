from fastapi import FastAPI
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Inicializa a tua API
app = FastAPI(title="Fábrica de Prompts Premium API")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# O teu "Endpoint" (a morada que os clientes vão chamar)
@app.get("/otimizar-prompt")
def otimizar_prompt(ideia_simples: str):
    """
    Esta função recebe uma ideia simples e devolve um prompt profissional.
    """
    print(f"[API] Pedido recebido para: {ideia_simples}")
    
    prompt_sistema = (
        "És um engenheiro de prompts especialista em Stable Diffusion e Midjourney. "
        "Transforma o conceito do utilizador num prompt em inglês altamente detalhado, "
        "cinematográfico e com especificações de iluminação. Devolve apenas o prompt final."
    )
    
    try:
        resposta = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": ideia_simples}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.6,
        )
        
        prompt_final = resposta.choices[0].message.content.strip()
        
        # O que a tua API responde de volta para o cliente
        return {
            "status": "sucesso",
            "conceito_original": ideia_simples,
            "prompt_otimizado": prompt_final
        }
        
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

# Comando para correr o servidor localmente
# No terminal escreverias: uvicorn api_fabrica:app --reload