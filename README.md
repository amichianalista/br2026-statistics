# Amichi Score | BR 2026

Aplicacao Streamlit para navegar jogadores e elencos do Brasileirao 2026.

## Executar localmente

1. Crie e ative um ambiente virtual.
2. Instale as dependencias com `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e preencha as credenciais do Supabase.
4. Rode `streamlit run app.py`.

## Publicar no Streamlit App

1. Suba este repositorio para o Git sem incluir `.env`.
2. No painel do Streamlit App, configure os secrets com base em `.streamlit/secrets.toml.example`.
3. Defina `app.py` como arquivo principal da aplicacao.

O app prioriza `SUPABASE_URL` com `SUPABASE_SECRET_KEY` ou `SUPABASE_SERVICE_ROLE_KEY` para ler as tabelas do schema `br_2026` pela API do Supabase. Se preferir, ele ainda aceita fallback por Postgres direto com `DATABASE_*` ou `DATABASE_URL`.
