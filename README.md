# 🛡️ Remediação de Código com Inteligência Artificial

## 📌 Sobre o Projeto
Este projeto demonstra o uso de Inteligência Artificial para automatizar o ciclo de **Code Review de Segurança**. O script lê um código Python vulnerável a SQL Injection e utiliza o Google Gemini para gerar um relatório técnico de auditoria e o código corrigido usando *Prepared Statements*.

## 🛠️ Tecnologias Utilizadas
* Python 3
* Google Gemini API (Modelo `gemini-3.6-flash`)
* SQLite (Para simular o banco de dados)

## ⚙️ Como Funciona
1. O script `fix_ia.py` lê o arquivo `app_vulneravel.py` (que contém a falha).
2. Envia o código para a IA com um prompt de "Engenheiro de Segurança Sênior".
3. A IA analisa a falha (CWE-89), explica o risco e gera um código corrigido.
4. O relatório final é salvo no arquivo `app_corrigido.md`.

## 🚀 Como Executar
1. Clone o repositório.
2. Crie um ambiente virtual: `python3 -m venv venv`
3. Ative o ambiente: `source venv/bin/activate`
4. Instale as dependências: `pip install google-genai python-dotenv`
5. Crie um arquivo `.env` com a sua `GEMINI_API_KEY`.
6. Execute: `python fix_ia.py`
