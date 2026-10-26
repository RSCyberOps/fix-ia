Como Engenheiro de Segurança Sênior, analisei o código fornecido. Abaixo está a avaliação detalhada da vulnerabilidade, a correção arquitetural e o exemplo de uso seguro.

---

### 1. O que está errado? (Análise da Vulnerabilidade)

O problema crítico neste código é a **concatenação direta de strings** para construir a consulta SQL (`query = "SELECT ... + user_input + "'"`). 

Essa prática viabiliza a vulnerabilidade de **SQL Injection (CWE-89)** pelos seguintes motivos:

1. **Mistura de Código e Dados:** O interpretador SQL do banco de dados não consegue diferenciar o que é instrução de código (escrita pelo desenvolvedor) do que é dado estático (enviado pelo usuário).
2. **Quebra de Contexto:** Quando o atacante envia a entrada `1' OR '1'='1`, a aspa simples (`'`) fecha precocemente a string esperada no parâmetro `id`. O restante do texto (`OR '1'='1`) é interpretado pelo banco de dados como **comandos SQL válidos**.
3. **Impacto:** A consulta resultante torna-se `SELECT * FROM users WHERE id = '1' OR '1'='1'`. Como `'1'='1'` é uma condição sempre verdadeira (*true*), o banco de dados retornará **todos** os registros da tabela `users`, burlando a autenticação ou expondo dados confidenciais.

---

### 2. Código Corrigido (Usando *Prepared Statements*)

Para corrigir a falha, devemos utilizar **Consultas Parametrizadas (Prepared Statements)**. 

Em uma consulta parametrizada, a estrutura da query SQL é enviada e compilada pelo banco de dados **antes** da inserção dos dados do usuário. O banco de dados garante que o valor do parâmetro seja tratado estritamente como um **dado estático (string/número)**, e nunca como código executável.

Abaixo está o código reescrito usando a biblioteca padrão `sqlite3` do Python para demonstrar o comportamento no mundo real:

```python
import sqlite3

# CÓDIGO CORRIGIDO (SEGURO)


def criar_banco_em_memoria():
    """Cria um banco de dados temporário para testes."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)"
    )
    cursor.execute(
        "INSERT INTO users (id, username, role) VALUES (1, 'admin', 'administrator')"
    )
    cursor.execute(
        "INSERT INTO users (id, username, role) VALUES (2, 'alice', 'user')"
    )
    conn.commit()
    return conn


def login_seguro(cursor, user_input):
    """Executa a busca de usuário de forma segura usando Prepared Statements.

    O caractere '?' atua como um placeholder para o parâmetro.
    """
    # 1. A estrutura do SQL é fixa (usando '?' como placeholder no SQLite)
    query = "SELECT * FROM users WHERE id = ?"

    print(f"\n--- Executando busca segura para o input: {repr(user_input)} ---")

    # 2. O input é passado separadamente na tupla (user_input,)
    # O driver do banco garante que a entrada seja tratada puramente como DADO.
    cursor.execute(query, (user_input,))

    resultados = cursor.fetchall()
    return resultados
```

---

### 3. Como o código deve ser usado de forma segura

Abaixo está a demonstração de execução. Observe como o ataque que antes funcionava agora falha com segurança, pois o banco procura por um ID que seja literalmente o texto `"1' OR '1'='1"`.

```python
if __name__ == "__main__":
    # Inicializa o banco de dados de teste
    conexao = criar_banco_em_memoria()
    cursor = conexao.cursor()

    # TESTE 1: Entrada Normal
    print("[+] Teste 1: Entrada normal (ID 1)")
    usuario = login_seguro(cursor, "1")
    print(f"Resultado retornado: {usuario}")
    # Retorna: [(1, 'admin', 'administrator')]

    # TESTE 2: Tentativa de SQL Injection
    print("\n[+] Teste 2: Tentativa de Ataque SQL Injection")
    ataque = "1' OR '1'='1"
    usuario = login_seguro(cursor, ataque)
    print(f"Resultado retornado: {usuario}")
    # Retorna: [] (Nenhum registro encontrado, pois não existe ID com esse texto exato)

    conexao.close()
```

### Resumo das Boas Práticas de Segurança:
* **Nunca** use concatenação de strings (`+`), interpolação (`f"SELECT ... {input}"`) ou `%s` direto na string para formatar SQL.
* **Sempre** passe os argumentos no método `.execute(query, (parametros,))`.
* Se estiver usando um ORM (como SQLAlchemy ou Django ORM), utilize os métodos nativos de abstração de consultas, pois eles já implementam consultas parametrizadas por padrão.