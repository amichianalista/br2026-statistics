# Amichi Score | BR 2026

Aplicacao Streamlit para navegar jogadores e elencos do Brasileirao 2026.

## Executar localmente

1. Crie e ative um ambiente virtual.
2. Instale as dependencias com `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e preencha as credenciais do banco.
4. Rode `streamlit run app.py`.

## Publicar no Streamlit App

1. Suba este repositorio para o Git sem incluir `.env`.
2. No painel do Streamlit App, configure os secrets com base em `.streamlit/secrets.toml.example`.
3. Defina `app.py` como arquivo principal da aplicacao.

Voce pode informar as credenciais com campos separados (`DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_SSLMODE`) ou usar apenas `DATABASE_URL`.
