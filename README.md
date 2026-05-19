# Amichi Score | BR 2026

Aplicacao Reflex para navegar jogadores e elencos do Brasileirao 2026 com uma interface premium, mobile-first e conectada ao Supabase.

## Executar localmente

1. Crie e ative um ambiente virtual.
2. Instale as dependencias com `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e preencha as credenciais do Supabase.
4. Rode `python -m reflex run`.

Em ambiente local, a interface normalmente sobe em `http://localhost:3000`.

## Estrutura principal

- `amichi_reflex/`: app Reflex, estado, paginas, componentes e servicos
- `assets/`: fundos e CSS global do frontend
- `rxconfig.py`: configuracao do app Reflex

## Dados e configuracao

O app usa `SUPABASE_URL` com `SUPABASE_SECRET_KEY` para ler os dados pela API do Supabase. Opcionalmente, voce pode definir `SUPABASE_SCHEMA`; se nada for informado, o app usa `public`. Os buckets `SUPABASE_BUCKET_TEAMS` e `SUPABASE_BUCKET_PLAYERS` sao usados para resolver imagens quando a base traz apenas o caminho do arquivo, e o app cai em placeholders visuais quando a imagem nao existe.
