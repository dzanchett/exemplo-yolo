# Dockerfile para Projeto de Detecção de Gado com YOLOv8
# =======================================================
# Este Dockerfile cria um container com todas as dependências
# necessárias para executar o projeto de detecção de gado.

# Usa imagem oficial do Python 3.10 (slim para reduzir tamanho)
FROM python:3.10-slim

# Define informações do maintainer
LABEL maintainer="Projeto Educacional YOLO"
LABEL description="Container para detecção e contagem de gado usando YOLOv8"

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para OpenCV
# - libgl1-mesa-glx: suporte OpenGL
# - libglib2.0-0: bibliotecas GLib
# - libsm6, libxext6, libxrender-dev: suporte X11
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências Python
# --no-cache-dir: não mantém cache (reduz tamanho da imagem)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script principal para o container
COPY detect_cattle.py .

# Cria diretórios necessários
RUN mkdir -p /workspace/images /workspace/output

# Define o volume para as imagens
# Isso permite montar diretórios do host no container
VOLUME ["/workspace/images", "/workspace/output"]

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Comando padrão ao executar o container
# Executa o script de detecção
CMD ["python", "detect_cattle.py"]
