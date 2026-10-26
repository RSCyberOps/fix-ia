import os
from google import genai
from dotenv import load_dotenv

# 1. Carrega a chave
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERRO: Chave da API não encontrada.")
    exit(1)

client = genai.Client(api_key=api_key)

# 2. Lê o código vulnerável
def ler_codigo(caminho):
    with open(caminho, 'r') as f:
        return f.read()

# 3. Função principal
def main():
    print("🔍 Lendo o código vulnerável...")
    codigo = ler_codigo("app_vulneravel.py")
    
    print("🤖 Enviando para a IA analisar e sugerir a correção...\n")
    
    prompt = f"""
    Você é um engenheiro de segurança sênior. Analise o código Python abaixo.
    Ele contém uma falha grave de SQL Injection.
    
    1. Explique em português o que está errado.
    2. Reescreva o código corrigido usando a técnica de "Prepared Statements" 
       (consultas parametrizadas) para evitar a falha.
    3. Mostre como o código deve ser usado de forma segura.

    Código vulnerável:
    {codigo}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        print("="*50)
        print("🛡️ RELATÓRIO DE REMEDIAÇÃO DA IA 🛡️")
        print("="*50)
        print(response.text)
        
        # Salva a correção em um arquivo
        with open("app_corrigido.md", "w") as f:
            f.write(response.text)
        print("\n✅ Correção salva em 'app_corrigido.md'")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
