# ---- Base ----
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o restante do projeto
COPY . .

# Define variáveis de ambiente do Flask
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=production
ENV PORT=8080

# Expõe a porta usada pelo Fly.io
EXPOSE 8080

# Comando de inicialização do servidor
# Gunicorn é mais performático que o servidor nativo do Flask
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:create_app()"]
