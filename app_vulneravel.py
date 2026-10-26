# CÓDIGO VULNERÁVEL (PARA ESTUDO)
# Este código simula a falha de SQL Injection do DVWA.

def login_vulneravel(user_input):
    # Simulação da query SQL que o servidor monta
    query = "SELECT * FROM users WHERE id = '" + user_input + "'"
    
    print(f"--- Query executada no servidor (Vulnerável) ---")
    print(query)
    print("------------------------------------------------")
    
    # Simulação do que o atacante pode fazer
    if "OR" in query.upper() or "UNION" in query.upper():
        print("🚨 ALERTA: O input do usuário alterou a estrutura da query SQL!")
        print("   Isso é uma SQL Injection!")
    else:
        print("✅ Query executada normalmente.")

if __name__ == "__main__":
    # Simulando um ataque
    print("Teste 1: Entrada normal")
    login_vulneravel("1")
    
    print("\nTeste 2: Entrada maliciosa")
    login_vulneravel("1' OR '1'='1")
