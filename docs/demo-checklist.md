# Demo Checklist | Amichi Score Reflex

## Subir localmente

```powershell
cd "d:\SofaAmichi\App Amichi Score\BR 2026"
.\.venv\Scripts\python.exe -m reflex run
```

Em ambiente local, a interface normalmente abre em:

- `http://localhost:3000`

## Ordem sugerida para apresentar

1. Abrir a Home e contextualizar o projeto como leitura visual do Brasileirao 2026.
2. Mostrar o hero principal e destacar o posicionamento mobile-first.
3. Demonstrar os filtros por clube, posicao e busca.
4. Explicar o bloco `Atleta em foco` como leitura editorial do catalogo.
5. Abrir uma ficha premium de jogador.
6. Destacar hero, metricas, tabs e a coluna lateral de executive summary.
7. Fechar explicando que os dados continuam vindo do Supabase, mas a interface foi refatorada para Reflex.

## Frases que ajudam na banca

- "Eu preservei a camada de dados em Python e refatorei a camada de apresentacao para uma experiencia mais profissional."
- "O objetivo nao foi apenas trocar framework, mas elevar hierarquia visual, navegacao e responsividade real."
- "A ficha do jogador foi desenhada para funcionar como tela de impacto e ao mesmo tempo como interface de leitura rapida."

## Pontos tecnicos para citar

- `Supabase` como origem dos dados
- normalizacao e enriquecimento de campos em Python
- `Reflex` para UI e estado
- separacao entre `services`, `state`, `pages` e `components`
- compilacao validada com export do frontend
