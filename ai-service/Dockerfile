FROM python:3.12-slim

# Instalar dependências de compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar pacotes Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); print('✅ Modelo sentence-transformers carregado')"

# Copiar código do projeto
COPY . .

# Expor porta padrão do Fastapi
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
