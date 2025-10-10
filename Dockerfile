# ---- Base ----
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o restante do projeto
COPY . .

# Define variáveis de ambiente para o Flask
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=production
ENV PORT=8080

# Expõe porta que o Fly.io usa
EXPOSE 8080

# Comando de inicialização
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:8080", "-w", "2"]
