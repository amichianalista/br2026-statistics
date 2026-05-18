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

O app usa `SUPABASE_URL` com `SUPABASE_SECRET_KEY` para ler os dados pela API do Supabase. Opcionalmente, voce pode definir `SUPABASE_SCHEMA`; se nada for informado, o app usa `public`. Os buckets `SUPABASE_BUCKET_TEAMS` e `SUPABASE_BUCKET_PLAYERS` sao usados para resolver imagens quando a base traz apenas o caminho do arquivo, e o app cai em placeholders visuais quando a imagem nao existe.
