# Luiz Esquivel — Site protótipo (Flask)

Este repositório contém um protótipo completo em **Flask** para publicar os seus textos com um painel administrativo.
Ele foi entregue como pedido por Luiz Esquivel (persona criativa) com foco em elegância, simplicidade e profundidade.

## Principais características
- Frontend com templates Jinja reutilizáveis (componentes em `templates/components/macros.html`).
- CSS com variáveis `:root` em `static/css/main.css`.
- Painel administrativo com autenticação (Flask-Login).
- CRUD de Seções e Textos (textos em Markdown).
- Renderização de Markdown via `markdown2`.
- Banco SQLite por padrão; suporte a `FLASK_APP` + `flask db` (Flask-Migrate) incluído.
- Seed automático no primeiro `flask run` (cria admin + seções iniciais).

## Como rodar (modo rápido)
1. Crie e ative um ambiente virtual (recomendado).
2. Instale dependências:
```bash
pip install -r requirements.txt
```
3. Copie `.env.example` para `.env` e ajuste `SECRET_KEY`, `ADMIN_EMAIL` e `ADMIN_PASSWORD` se desejar.
4. Rodar a aplicação:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask db init    # só se for a primeira vez (podem já existir arquivos de migrations do protótipo)
flask db migrate -m "create tables"
flask db upgrade
flask run
```
A aplicação cria o banco e faz o *seed* com um usuário admin (valores por padrão do `.env.example`) na primeira execução.

## Como usar `flask db` (opcional - Flask-Migrate)
Este projeto inclui Flask-Migrate e está pronto para ser usado. Para utilizar migrações:
```bash
export FLASK_APP=app.py
flask db init    # só se for a primeira vez (podem já existir arquivos de migrations do protótipo)
flask db migrate -m "create tables"
flask db upgrade
```
> Observação: O protótipo já faz `db.create_all()` no startup se preferir pular migrações.

## Credenciais iniciais (seed)
- Email: `admin@example.com`
- Senha: `ChangeMe123!`

Altere imediatamente no `.env` ou no painel (não existe ainda UI para trocar senha no protótipo básico).

## Estrutura chave
- `app.py` — ponto de entrada e rotas.
- `models.py` — modelos SQLAlchemy.
- `forms.py` — formulários Flask-WTF.
- `templates/` — templates Jinja (público e admin).
- `static/css/main.css` — tema com `:root` variables.
- `static_files/` — local para colocar ebooks públicos (ex: PDF).
- `seed.py` — exemplo de script de seed (já embutido no `app.py` via before_first_request).

## Como publicar textos
1. Faça login em `/admin/login` com as credenciais do seed.
2. Crie/edite seções em "Seções".
3. Crie textos em "Novo Texto". Use Markdown (ex: parágrafos, listas, **negrito**, _italico_, links).
4. Publique para torná-lo visível ao público.

## Observações finais
- O projeto foi pensado para ser simples, limpo e fácil de modificar.
- Se você quiser, eu posso:
  - Gerar um design Figma / protótipo visual.
  - Converter o painel para React ou Next.js.
  - Adicionar suporte a upload direto para o Google Drive.
  - Implementar A/B testing e analytics.

Edite o projeto à vontade — as principais variáveis de estilo estão em `static/css/main.css` (:root), e textos de conteúdo aparecem em `templates` e no banco SQLite (`luis_site.db`).
