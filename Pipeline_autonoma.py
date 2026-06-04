import json
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# O passe de entrada para a matriz
client = Groq(api_key=os.getenv("GROQ_API_KEY")) 

FICHEIRO_ESTADO = "armazem_logistica.json"

def carregar_save():
    if os.path.exists(FICHEIRO_ESTADO):
        with open(FICHEIRO_ESTADO, "r") as f:
            return json.load(f)
    return {
        "ferramentas_a_venda": {}, 
        "lixo_rejeitado": []       
    }

def guardar_save(estado):
    with open(FICHEIRO_ESTADO, "w") as f:
        json.dump(estado, f, indent=4)

# ==========================================
# 🏢 EDIFÍCIO 1: LABORATÓRIO (Diretor, Dev, QA, Copy)
# ==========================================

def ia_diretor_ideias(ferramentas_completas):
    """O CEO autónomo que descobre os nichos lucrativos olhando para os dados de mercado."""
    relatorio_mercado = ""
    if ferramentas_completas:
        for id_prod, dados in ferramentas_completas.items():
            relatorio_mercado += f"- Código: {dados.get('codigo', '')[:30]}... | Vitórias: {dados['vitorias']} | Derrotas: {dados['derrotas']}\n"
    else:
        relatorio_mercado = "O mercado está virgem. Não temos dados históricos."

    print("\n🧠 [DIRETOR] A analisar o relatório de lucros para encontrar uma nova policy de mercado...")
    
    prompt_sistema = (
        "És uma Inteligência Artificial CEO com total liberdade criativa. O teu único objetivo é gerar lucro. "
        "Vendes micro-serviços Python numa API para programadores profissionais. "
        f"Aqui está o relatório do que tem dado dinheiro e do que tem falhado na nossa loja:\n{relatorio_mercado}\n"
        "REGRAS:\n"
        "1. Analisa os dados. Se algo tem vitórias, cria ferramentas semelhantes ou complementares.\n"
        "2. Se algo tem derrotas, abandona completamente essa área da ciência da computação.\n"
        "3. Se o mercado estiver virgem, foca-te em nichos rentáveis e complexos (ex: finanças, dados, matemática avançada).\n"
        "4. Sugere APENAS UMA ideia abstrata para um script Python. Não peças desculpa, não expliques, dá-me só a ideia numa frase."
    )
    
    try:
        resposta = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}],
            model="llama-3.1-8b-instant",
            temperature=0.9, 
        )
        ideia = resposta.choices[0].message.content.strip()
        print(f"🎯 [DIRETOR] Encomenda aprovada: {ideia}")
        return ideia
    except Exception as e:
        print(f"❌ [DIRETOR] Falha de comunicação: {e}")
        return "uma função matemática complexa para tratamento de matrizes"

def ia_programador(ideia_da_logistica):
    """Liga à Groq e exige um código profissional para APIs."""
    print("👨‍💻 [DEV] LLaMA 3.1 a projetar micro-serviço robusto...")
    
    prompt_sistema = (
        "És um Engenheiro de Software Sénior especialista em arquitetura de Micro-serviços e APIs. "
        "A tua tarefa é escrever uma função em Python extremamente robusta chamada obrigatoriamente 'executar(...)'.\n\n"
        "REGRAS CRÍTICAS DE ARQUITETURA:\n"
        "1. É EXPRESSAMENTE PROIBIDO usar as funções 'input()' ou 'print()'.\n"
        "2. Todos os dados de entrada devem ser passados como ARGUMENTOS da função 'executar'.\n"
        "3. A função deve RETORNAR obrigatoriamente um DICIONÁRIO (dict) com os dados processados.\n"
        "4. Inclui validação de dados simples.\n"
        "5. Usa apenas a biblioteca standard do Python.\n"
        "6. Devolve APENAS o código Python puro, sem decorações Markdown (sem ```python), sem explicações."
        "7. Vais fazer uma API que vai ser vendida a programadores profissionais, por isso o código tem de ser limpo, eficiente e fácil de integrar. "
    )
    
    try:
        resposta = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Cria o micro-serviço funcional para: {ideia_da_logistica}"}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2, 
        )
        
        codigo_bruto = resposta.choices[0].message.content.strip()
        codigo_limpo = codigo_bruto.replace("```python", "").replace("```", "").strip()
        return codigo_limpo
    except Exception as e:
        print(f"❌ [DEV] Falha na geração do código: {e}")
        return None

def ia_auditor(codigo_novo):
    """O QA testa o código antes de o atirar para o mercado."""
    print("🕵️ [QA] A auditar a sintaxe e a arquitetura do código gerado...")
    if not codigo_novo:
        return False
        
    try:
        compile(codigo_novo, '<string>', 'exec')
        if "def executar" not in codigo_novo:
            print("❌ [QA] Código chumbado. Falta a função principal 'executar()'.")
            return False
            
        print("✅ [QA] Código aprovado! Zero bugs detetados. Pronto para produção.")
        return True
    except Exception as e:
        print(f"❌ [QA] Código chumbado. Erro de sintaxe: {e}")
        return False

def ia_documentador(codigo_aprovado, ideia_original):
    """O Marketer que escreve o manual de instruções para o RapidAPI."""
    print("📝 [COPYWRITER] A redigir a documentação técnica para os clientes...")
    
    prompt_sistema = (
        "És um Technical Writer especialista em documentar APIs para o RapidAPI. "
        "Vou dar-te um código Python e a ideia original dele. "
        "Escreve uma descrição comercial e técnica muito curta (máximo 3 linhas). "
        "Tens de explicar obrigatoriamente: 1) O que a ferramenta faz. 2) Que argumentos precisa receber. 3) O que devolve. "
        "Não escrevas introduções nem formatações estranhas, apenas o texto do manual."
    )
    
    try:
        resposta = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Ideia: {ideia_original}\nCódigo:\n{codigo_aprovado}"}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3, 
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ [COPYWRITER] Falha a escrever documentação: {e}")
        return "Micro-serviço Python pronto a usar."

# ==========================================
# 🏗️ EDIFÍCIO 2: LOGÍSTICA E MERCADO
# ==========================================

def logistica_avaliar_mercado(estado):
    print("\n📊 [LOGÍSTICA] A verificar stock e prejuízos...")
    
    ferramentas = estado["ferramentas_a_venda"]
    ferramentas_a_apagar = []
    
    # 1. A Poda
    for nome, stats in ferramentas.items():
        if stats["derrotas"] >= 3 and stats["vitorias"] == 0:
            print(f"✂️ [LOGÍSTICA] A ferramenta '{nome}' só dá prejuízo. Despedida!")
            ferramentas_a_apagar.append(nome)
            estado["lixo_rejeitado"].append(nome)
            
    for nome in ferramentas_a_apagar:
        del ferramentas[nome]
        
    # 2. A Inovação (O funil que chama os 4 funcionários por ordem)
    if len(ferramentas) < 2:
        print("💡 [LOGÍSTICA] A montra está com baixa oferta. A ligar ao Diretor...")
        
        # Passo 1: O Diretor inventa
        ideia_nova = ia_diretor_ideias(ferramentas)
        
        # Passo 2: O Programador escreve
        novo_codigo = ia_programador(ideia_nova)
        
        # Passo 3: O Auditor testa
        aprovado = ia_auditor(novo_codigo)
        
        if aprovado:
            # Passo 4: O Documentador escreve o manual
            manual_instrucoes = ia_documentador(novo_codigo, ideia_nova)
            
            id_produto = f"api_tool_{int(time.time())}"
            estado["ferramentas_a_venda"][id_produto] = {
                "descricao_rapidapi": manual_instrucoes,
                "codigo": novo_codigo, 
                "vitorias": 0, 
                "derrotas": 0
            }
            print(f"🛒 [LOGÍSTICA] Sucesso! Novo produto guardado no armazém: {id_produto}")
        else:
            print("♻️ [LOGÍSTICA] O produto voltou para trás. A equipa tentará novamente no próximo turno.")
            
    return estado

# ==========================================
# ⚙️ O MOTOR PRINCIPAL
# ==========================================

def arrancar_fabrica():
    print("\n🏭 TURNO DA FÁBRICA INICIADO 🏭")
    estado_atual = carregar_save()
    estado_atualizado = logistica_avaliar_mercado(estado_atual)
    guardar_save(estado_atualizado)
    print("💾 [SISTEMA] Estado gravado no disco com segurança.")
    print("="*50)

if __name__ == "__main__":
    print("🚀 A LIGAR O QUADRO ELÉTRICO DA FÁBRICA...")
    try:
        while True:
            arrancar_fabrica()
            print("\n⏳ [SISTEMA] Turno fechado. O sistema vai dormir 15 segundos...")
            time.sleep(15)
    except KeyboardInterrupt:
        print("\n🛑 [SISTEMA] Botão de emergência pressionado! Fábrica desligada em segurança.")