# 🚀 Guia Rápido de Uso

## 📋 Pré-requisitos

### Opção 1: Docker (Recomendado) 🐳
- Docker instalado ([Instalar Docker](https://docs.docker.com/get-docker/))
- Docker Compose instalado ([Instalar Docker Compose](https://docs.docker.com/compose/install/))

### Opção 2: Local
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

---

## 🎯 Início Rápido (3 comandos)

### Com Docker:
```bash
# 1. Clone ou navegue até o diretório do projeto
cd /workspace

# 2. Construa a imagem (primeira vez apenas)
docker-compose build

# 3. Execute!
docker-compose up
```

### Sem Docker:
```bash
# 1. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute!
python detect_cattle.py
```

---

## 🎬 Usando o Script Auxiliar (Mais Fácil!)

O projeto inclui um script auxiliar que facilita tudo:

```bash
# Torne o script executável (primeira vez)
chmod +x run.sh

# Execute o menu interativo
./run.sh
```

### Opções do Script:

```bash
./run.sh docker    # Executa com Docker
./run.sh local     # Executa localmente
./run.sh build     # Constrói apenas a imagem
./run.sh clean     # Limpa outputs
./run.sh help      # Mostra ajuda
```

---

## 📁 Estrutura de Arquivos

### Antes da Execução:
```
workspace/
├── images/           # Suas imagens aqui
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
└── detect_cattle.py
```

### Depois da Execução:
```
workspace/
├── images/           # Imagens originais (sem modificações)
│   └── ...
├── output/           # ✨ Criado automaticamente
│   ├── detected_img1.jpg      # Imagens com detecções
│   ├── detected_img2.jpg
│   └── report.json             # Relatório detalhado
└── detect_cattle.py
```

---

## 📊 Entendendo os Resultados

### 1. Imagens Processadas

As imagens em `output/` terão:
- 🟢 **Retângulos verdes** ao redor dos animais detectados
- 🏷️ **Label** com classe e confiança (ex: "cow 0.95")

### 2. Relatório JSON

O arquivo `output/report.json` contém:

```json
{
  "total_images": 4,
  "total_cattle": 15,
  "processing_time": 2.34,
  "images_processed": [
    {
      "filename": "img1.jpg",
      "cattle_count": 3,
      "detections": [
        {
          "class": "cow",
          "confidence": 0.95,
          "bbox": [120, 150, 300, 400]
        }
      ],
      "output_path": "/workspace/output/detected_img1.jpg"
    }
  ]
}
```

### 3. Saída no Console

```
╔══════════════════════════════════════════════════════════╗
║   🐄 Sistema de Detecção e Contagem de Gado - YOLOv8   ║
╚══════════════════════════════════════════════════════════╝

📦 Carregando modelo YOLO: yolov8n.pt
✅ Modelo carregado com sucesso!

🔍 Processando: img1.jpg
   🐄 Gado detectado: 3

📊 RESUMO DOS RESULTADOS
🖼️  Total de imagens processadas: 4
🐄 Total de gado detectado: 15
⏱️  Tempo de processamento: 2.34 segundos
```

---

## ⚙️ Personalizações

### 1. Mudar o Modelo YOLO

Edite `detect_cattle.py` (linha ~448):

```python
# Mais rápido, menos preciso
MODEL_NAME = 'yolov8n.pt'  # ⚡⚡⚡ (padrão)

# Balanceado
MODEL_NAME = 'yolov8m.pt'  # ⚡⚡

# Mais preciso, mais lento
MODEL_NAME = 'yolov8l.pt'  # ⚡
```

### 2. Ajustar Confiança Mínima

Edite `detect_cattle.py` (linha ~451):

```python
CONFIDENCE_THRESHOLD = 0.25  # Padrão

# Mais detecções (pode ter falsos positivos)
CONFIDENCE_THRESHOLD = 0.15

# Menos detecções (mais conservador)
CONFIDENCE_THRESHOLD = 0.50
```

### 3. Processar Outras Imagens

Simplesmente coloque suas imagens no diretório `images/`:

```bash
cp minhas_fotos/*.jpg images/
./run.sh docker  # ou local
```

---

## 🐛 Solução de Problemas

### Erro: "Docker não encontrado"
```bash
# Instale o Docker
# Linux (Ubuntu/Debian):
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ou siga: https://docs.docker.com/get-docker/
```

### Erro: "No module named 'ultralytics'"
```bash
# Certifique-se de estar no ambiente virtual
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "libGL.so.1: cannot open shared object file"
```bash
# Linux (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install libgl1-mesa-glx

# Ou use Docker (evita problemas de dependências do sistema)
./run.sh docker
```

### Imagens não sendo detectadas
1. **Verifique as imagens**: Estão no diretório `images/`?
2. **Formato correto**: `.jpg`, `.jpeg`, `.png`?
3. **Ajuste a confiança**: Tente `CONFIDENCE_THRESHOLD = 0.15`
4. **Use modelo maior**: Troque para `yolov8m.pt` ou `yolov8l.pt`

### Performance lenta
1. **Use modelo menor**: `yolov8n.pt` (mais rápido)
2. **Docker**: Limite recursos no `docker-compose.yml`
3. **GPU**: Se disponível, PyTorch usará automaticamente

---

## 💡 Dicas Avançadas

### 1. Processar Apenas Uma Imagem
```bash
python detect_cattle.py
# Depois modifique o código para processar apenas uma imagem específica
```

### 2. Integrar com Outros Scripts
```python
from detect_cattle import CattleDetector

detector = CattleDetector()
image_path = "minha_imagem.jpg"
processed_img, count, detections = detector.detect_in_image(image_path)
print(f"Detectados: {count} animais")
```

### 3. Batch Processing em GPU
```python
# No detect_cattle.py, use:
results = self.model(images, device='cuda')  # GPU
# ou
results = self.model(images, device='cpu')   # CPU
```

### 4. Salvar Apenas o Relatório (sem imagens)
```python
# Comente as linhas de cv2.imwrite() se não precisar das imagens
# Mantenha apenas a geração do JSON
```

---

## 📞 Precisa de Ajuda?

1. **Leia a documentação completa**: `README.md`
2. **Entenda o YOLO**: `YOLO_EXPLICADO.md`
3. **Verifique os logs**: Mensagens de erro geralmente indicam o problema
4. **Docker recomendado**: Evita problemas de dependências

---

## ✅ Checklist de Execução

- [ ] Docker ou Python instalado
- [ ] Imagens no diretório `images/`
- [ ] Executou `chmod +x run.sh` (se usando o script)
- [ ] Executou o comando apropriado (`docker-compose up` ou `python detect_cattle.py`)
- [ ] Verificou a pasta `output/` para resultados

---

**Pronto para começar! 🚀**

```bash
# Execução em 1 linha:
./run.sh docker
```

🎉 **Simples assim!**
