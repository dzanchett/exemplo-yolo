# 🐄 Sistema de Detecção e Contagem de Gado usando YOLOv8

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-green)

## 📚 Sobre o Projeto

Este é um projeto **educacional e didático** que demonstra como utilizar o **YOLOv8** (You Only Look Once versão 8) para detectar e contar gado (bovinos) em imagens. O código foi desenvolvido com foco em clareza e facilidade de compreensão, sendo ideal para estudantes e profissionais que desejam aprender sobre detecção de objetos com Deep Learning.

### 🎯 Objetivos do Projeto

- ✅ Demonstrar o uso prático do YOLOv8 para detecção de objetos
- ✅ Ensinar conceitos de visão computacional de forma didática
- ✅ Mostrar como conteinerizar aplicações de ML com Docker
- ✅ Fornecer código limpo e bem comentado para fins educacionais
- ✅ Aplicação prática: contagem automatizada de gado em fazendas

## 🏗️ Arquitetura do Projeto

```
workspace/
│
├── detect_cattle.py       # Script principal (código didático)
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração do container
├── docker-compose.yml    # Orquestração Docker simplificada
├── .dockerignore         # Arquivos ignorados pelo Docker
├── README.md             # Este arquivo
│
├── images/               # Diretório com imagens de entrada
│   ├── img1.jpg
│   ├── img2.jpg
│   ├── img3.jpg
│   └── img4.jpeg
│
└── output/               # Diretório de saída (criado automaticamente)
    ├── detected_img1.jpg
    ├── detected_img2.jpg
    ├── detected_img3.jpg
    ├── detected_img4.jpeg
    └── report.json       # Relatório JSON com resultados
```

## 🧠 Como Funciona

### 1. **Modelo YOLOv8**
O projeto utiliza o YOLOv8 da Ultralytics, um dos modelos de detecção de objetos mais modernos e eficientes. O modelo foi treinado no dataset COCO, que inclui a classe "cow" (vaca/boi).

### 2. **Pipeline de Processamento**
```
Imagem → YOLOv8 → Detecção → Filtro (apenas bovinos) → Contagem → Visualização
```

### 3. **Componentes Principais**

- **CattleDetector**: Classe principal que encapsula toda a lógica
  - Carrega o modelo YOLO
  - Processa imagens individuais
  - Detecta e conta bovinos
  - Gera visualizações e relatórios

## 🚀 Como Usar

### Opção 1: Usando Docker (Recomendado) 🐳

**Passo 1:** Certifique-se de ter o Docker instalado
```bash
docker --version
docker-compose --version
```

**Passo 2:** Construa a imagem Docker
```bash
docker-compose build
```

**Passo 3:** Execute o container
```bash
docker-compose up
```

Ou execute diretamente com Docker:
```bash
# Construir a imagem
docker build -t cattle-detector .

# Executar o container
docker run --rm \
  -v $(pwd)/images:/workspace/images:ro \
  -v $(pwd)/output:/workspace/output:rw \
  cattle-detector
```

### Opção 2: Executando Localmente (sem Docker)

**Passo 1:** Certifique-se de ter Python 3.10+ instalado
```bash
python --version
```

**Passo 2:** Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

**Passo 3:** Instale as dependências
```bash
pip install -r requirements.txt
```

**Passo 4:** Execute o script
```bash
python detect_cattle.py
```

## 📊 Resultados

Após a execução, você encontrará:

### 1. **Imagens Processadas** (`output/`)
- Imagens com bounding boxes desenhados ao redor dos animais detectados
- Cada detecção mostra a classe e a confiança da predição
- Formato: `detected_[nome_original].jpg`

### 2. **Relatório JSON** (`output/report.json`)
```json
{
  "total_images": 4,
  "total_cattle": 15,
  "processing_time": 2.34,
  "images_processed": [
    {
      "filename": "img1.jpg",
      "cattle_count": 3,
      "detections": [...]
    }
  ]
}
```

### 3. **Saída no Console**
```
╔══════════════════════════════════════════════════════════╗
║   🐄 Sistema de Detecção e Contagem de Gado - YOLOv8   ║
║              Projeto Educacional                         ║
╚══════════════════════════════════════════════════════════╝

📦 Carregando modelo YOLO: yolov8n.pt
   Confiança mínima: 0.25
✅ Modelo carregado com sucesso!

🔍 Processando: img1.jpg
   🐄 Gado detectado: 3

📊 RESUMO DOS RESULTADOS
🖼️  Total de imagens processadas: 4
🐄 Total de gado detectado: 15
⏱️  Tempo de processamento: 2.34 segundos
```

## 🎓 Conceitos Didáticos Abordados

### 1. **Deep Learning e Redes Neurais**
- Como funcionam modelos de detecção de objetos
- Arquitetura YOLO (You Only Look Once)
- Transfer Learning com modelos pré-treinados

### 2. **Visão Computacional**
- Processamento de imagens com OpenCV
- Bounding boxes e visualizações
- Pós-processamento de detecções

### 3. **Engenharia de Software**
- Código orientado a objetos
- Documentação e comentários
- Tratamento de erros
- Type hints em Python

### 4. **DevOps e Containerização**
- Docker e Dockerfile
- Docker Compose
- Volumes e bind mounts
- Reprodutibilidade de ambientes

## ⚙️ Configurações Avançadas

### Modelos YOLOv8 Disponíveis

Você pode alterar o modelo no arquivo `detect_cattle.py`:

| Modelo | Tamanho | Velocidade | Precisão |
|--------|---------|------------|----------|
| `yolov8n.pt` | Nano | ⚡⚡⚡ | ⭐⭐ |
| `yolov8s.pt` | Small | ⚡⚡ | ⭐⭐⭐ |
| `yolov8m.pt` | Medium | ⚡ | ⭐⭐⭐⭐ |
| `yolov8l.pt` | Large | 🐌 | ⭐⭐⭐⭐⭐ |
| `yolov8x.pt` | Extra Large | 🐌🐌 | ⭐⭐⭐⭐⭐⭐ |

### Ajustar Threshold de Confiança

No arquivo `detect_cattle.py`, linha ~448:
```python
CONFIDENCE_THRESHOLD = 0.25  # Valores entre 0.0 e 1.0
```

- **Menor** (0.1-0.3): Detecta mais, mas pode ter falsos positivos
- **Médio** (0.25-0.5): Balanceado (recomendado)
- **Maior** (0.5-0.9): Mais conservador, menos falsos positivos

## 🔬 Limitações e Melhorias Futuras

### Limitações Atuais
- Usa modelo pré-treinado no COCO (não especializado em gado)
- Acurácia pode variar com condições de iluminação e ângulo
- Não distingue entre diferentes raças de gado

### Possíveis Melhorias
- [ ] Fine-tuning do modelo com dataset específico de gado
- [ ] Detecção em vídeos (stream processing)
- [ ] API REST para integração com outros sistemas
- [ ] Interface web para upload de imagens
- [ ] Tracking de animais individuais ao longo do tempo
- [ ] Classificação de raças bovinas
- [ ] Detecção de comportamentos anômalos

## 📦 Dependências Principais

- **ultralytics (8.0.220)**: Framework YOLOv8
- **opencv-python (4.8.1.78)**: Processamento de imagens
- **numpy (1.24.3)**: Operações numéricas
- **torch**: Motor de deep learning (instalado automaticamente)

## 🤝 Contribuindo

Este é um projeto educacional! Sugestões e melhorias são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## 👥 Autores

- **Projeto Educacional YOLO** - Desenvolvido para curso de Machine Learning

## 📚 Recursos Adicionais

### Documentação
- [YOLOv8 Official Docs](https://docs.ultralytics.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Docker Documentation](https://docs.docker.com/)

### Tutoriais Recomendados
- [Understanding YOLO](https://pjreddie.com/darknet/yolo/)
- [Object Detection Explained](https://arxiv.org/abs/1506.02640)
- [Transfer Learning Guide](https://cs231n.github.io/transfer-learning/)

## 🐛 Solução de Problemas

### Erro: "No module named 'ultralytics'"
```bash
pip install ultralytics
```

### Erro: "libGL.so.1: cannot open shared object file"
No Ubuntu/Debian:
```bash
sudo apt-get install libgl1-mesa-glx
```

### Docker não encontra as imagens
Certifique-se de que as imagens estão no diretório `./images/` e que o docker-compose está sendo executado do diretório raiz do projeto.

### Baixa acurácia
- Ajuste o `CONFIDENCE_THRESHOLD`
- Considere usar um modelo maior (yolov8m ou yolov8l)
- Verifique a qualidade das imagens de entrada

## 📞 Suporte

Para dúvidas e sugestões, abra uma issue no repositório do projeto.

---

**Desenvolvido com ❤️ para fins educacionais**

🎓 *Este projeto foi criado para demonstrar conceitos de Machine Learning e Deep Learning de forma prática e didática.*
