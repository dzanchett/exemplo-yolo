# 🚀 Exemplos Avançados - YOLOv8 Cattle Detection

Este documento contém exemplos avançados de uso e extensões do projeto para estudantes que desejam ir além do básico.

---

## 📋 Índice
1. [Usar o Detector como Módulo](#1-usar-o-detector-como-módulo)
2. [Processar Vídeos](#2-processar-vídeos)
3. [Detecção em Tempo Real (Webcam)](#3-detecção-em-tempo-real-webcam)
4. [API REST com FastAPI](#4-api-rest-com-fastapi)
5. [Interface Web com Streamlit](#5-interface-web-com-streamlit)
6. [Fine-tuning do Modelo](#6-fine-tuning-do-modelo)
7. [Batch Processing Paralelo](#7-batch-processing-paralelo)
8. [Salvar em Diferentes Formatos](#8-salvar-em-diferentes-formatos)

---

## 1. Usar o Detector como Módulo

### 1.1 Importar e Usar em Outro Script

```python
# meu_script.py
from detect_cattle import CattleDetector

# Inicializa o detector
detector = CattleDetector(
    model_name='yolov8m.pt',  # Modelo maior para mais precisão
    confidence=0.3
)

# Detecta em uma imagem
image_path = 'images/img1.jpg'
processed_img, count, detections = detector.detect_in_image(image_path)

print(f"🐄 Gado detectado: {count}")
for i, det in enumerate(detections, 1):
    print(f"  {i}. Confiança: {det['confidence']:.2f}, Bbox: {det['bbox']}")
```

### 1.2 Processar Imagem da Memória

```python
import cv2
from detect_cattle import CattleDetector

# Carrega imagem
image = cv2.imread('images/img1.jpg')

# Cria detector
detector = CattleDetector()

# Modifica o método detect_in_image para aceitar numpy array
# Ou trabalhe diretamente com o modelo YOLO:
results = detector.model(image, conf=0.25)

# Processa resultados
for result in results[0].boxes:
    class_id = int(result.cls[0])
    if class_id == 19:  # cow
        confidence = float(result.conf[0])
        bbox = result.xyxy[0].cpu().numpy()
        print(f"Vaca detectada: {confidence:.2f} @ {bbox}")
```

---

## 2. Processar Vídeos

### 2.1 Script Básico de Processamento de Vídeo

```python
# detect_video.py
import cv2
from ultralytics import YOLO

def process_video(video_path, output_path, model_name='yolov8n.pt'):
    """
    Processa um vídeo e detecta gado frame a frame.
    """
    # Carrega modelo
    model = YOLO(model_name)
    
    # Abre vídeo
    cap = cv2.VideoCapture(video_path)
    
    # Obtém propriedades do vídeo
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Configura writer de vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    cattle_per_frame = []
    
    print("🎬 Processando vídeo...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detecta no frame
        results = model(frame, conf=0.25, verbose=False)
        
        # Conta bovinos
        cattle_count = 0
        for box in results[0].boxes:
            if int(box.cls[0]) == 19:  # cow
                cattle_count += 1
        
        cattle_per_frame.append(cattle_count)
        
        # Desenha detecções no frame
        annotated_frame = results[0].plot()
        
        # Adiciona contagem no frame
        cv2.putText(
            annotated_frame,
            f"Gado: {cattle_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Escreve frame processado
        out.write(annotated_frame)
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"   Processados {frame_count} frames...")
    
    # Libera recursos
    cap.release()
    out.release()
    
    # Estatísticas
    print(f"\n✅ Vídeo processado!")
    print(f"   Total de frames: {frame_count}")
    print(f"   Média de gado: {sum(cattle_per_frame)/len(cattle_per_frame):.1f}")
    print(f"   Máximo: {max(cattle_per_frame)}")
    print(f"   Mínimo: {min(cattle_per_frame)}")

# Uso
if __name__ == "__main__":
    process_video('input.mp4', 'output.mp4', 'yolov8n.pt')
```

---

## 3. Detecção em Tempo Real (Webcam)

### 3.1 Script de Webcam

```python
# webcam_detector.py
import cv2
from ultralytics import YOLO
import time

def webcam_detection(model_name='yolov8n.pt'):
    """
    Detecta gado em tempo real usando webcam.
    Pressione 'q' para sair.
    """
    model = YOLO(model_name)
    cap = cv2.VideoCapture(0)  # 0 = webcam padrão
    
    if not cap.isOpened():
        print("❌ Não foi possível abrir a webcam!")
        return
    
    print("📹 Webcam ativa. Pressione 'q' para sair.")
    
    fps_counter = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detecta
        results = model(frame, conf=0.25, verbose=False)
        
        # Conta bovinos
        cattle_count = sum(1 for box in results[0].boxes if int(box.cls[0]) == 19)
        
        # Desenha
        annotated_frame = results[0].plot()
        
        # Calcula FPS
        fps_counter += 1
        elapsed = time.time() - start_time
        fps = fps_counter / elapsed if elapsed > 0 else 0
        
        # Adiciona informações
        cv2.putText(annotated_frame, f"Gado: {cattle_count}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", 
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Mostra
        cv2.imshow('Cattle Detection', annotated_frame)
        
        # Sai com 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n✅ FPS médio: {fps:.1f}")

if __name__ == "__main__":
    webcam_detection()
```

---

## 4. API REST com FastAPI

### 4.1 Instalar FastAPI

```bash
pip install fastapi uvicorn python-multipart
```

### 4.2 API Simples

```python
# api.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from detect_cattle import CattleDetector
import cv2
import numpy as np
import tempfile
import os

app = FastAPI(title="Cattle Detection API")
detector = CattleDetector(model_name='yolov8n.pt')

@app.get("/")
def root():
    return {"message": "🐄 Cattle Detection API"}

@app.post("/detect")
async def detect_cattle(file: UploadFile = File(...)):
    """
    Endpoint para detecção de gado em imagem.
    """
    # Lê imagem
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Imagem inválida"}
        )
    
    # Detecta
    results = detector.model(image, conf=0.25, verbose=False)
    
    # Conta bovinos
    cattle_count = 0
    detections = []
    
    for box in results[0].boxes:
        if int(box.cls[0]) == 19:  # cow
            cattle_count += 1
            detections.append({
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].cpu().numpy().tolist()
            })
    
    return {
        "filename": file.filename,
        "cattle_count": cattle_count,
        "detections": detections
    }

@app.post("/detect-and-save")
async def detect_and_save(file: UploadFile = File(...)):
    """
    Endpoint que retorna a imagem processada.
    """
    # Lê imagem
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detecta
    results = detector.model(image, conf=0.25, verbose=False)
    annotated_image = results[0].plot()
    
    # Salva temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
        cv2.imwrite(tmp.name, annotated_image)
        tmp_path = tmp.name
    
    return FileResponse(
        tmp_path,
        media_type="image/jpeg",
        filename=f"detected_{file.filename}"
    )

# Executar com: uvicorn api:app --reload
```

### 4.3 Testar a API

```bash
# Iniciar servidor
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Em outro terminal, testar:
curl -X POST "http://localhost:8000/detect" \
  -F "file=@images/img1.jpg"
```

---

## 5. Interface Web com Streamlit

### 5.1 Instalar Streamlit

```bash
pip install streamlit
```

### 5.2 App Streamlit

```python
# app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from detect_cattle import CattleDetector

# Configuração da página
st.set_page_config(
    page_title="🐄 Cattle Detector",
    page_icon="🐄",
    layout="wide"
)

# Título
st.title("🐄 Sistema de Detecção de Gado")
st.markdown("Upload uma imagem para detectar e contar bovinos usando YOLOv8")

# Sidebar
st.sidebar.header("⚙️ Configurações")
model_choice = st.sidebar.selectbox(
    "Modelo YOLO",
    ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt']
)
confidence = st.sidebar.slider("Confiança Mínima", 0.0, 1.0, 0.25, 0.05)

# Inicializa detector (cache para não recarregar)
@st.cache_resource
def load_detector(model_name):
    return CattleDetector(model_name=model_name, confidence=0.1)

detector = load_detector(model_choice)

# Upload de imagem
uploaded_file = st.file_uploader(
    "Escolha uma imagem...",
    type=['jpg', 'jpeg', 'png']
)

if uploaded_file is not None:
    # Lê imagem
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Layout em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Imagem Original")
        st.image(image_rgb, use_column_width=True)
    
    # Detecta
    with st.spinner('🔍 Detectando gado...'):
        results = detector.model(image, conf=confidence, verbose=False)
        
        # Conta bovinos
        cattle_count = 0
        detections_list = []
        
        for box in results[0].boxes:
            if int(box.cls[0]) == 19:  # cow
                cattle_count += 1
                detections_list.append({
                    "Confiança": f"{float(box.conf[0]):.2%}",
                    "Bbox": box.xyxy[0].cpu().numpy().tolist()
                })
        
        # Imagem anotada
        annotated = results[0].plot()
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    
    with col2:
        st.subheader("Detecções")
        st.image(annotated_rgb, use_column_width=True)
    
    # Resultados
    st.success(f"🐄 **Total de gado detectado: {cattle_count}**")
    
    # Tabela de detecções
    if detections_list:
        st.subheader("📋 Detalhes das Detecções")
        st.json(detections_list)
    
    # Botão de download
    _, encoded_img = cv2.imencode('.jpg', annotated)
    st.download_button(
        label="📥 Baixar Imagem Processada",
        data=encoded_img.tobytes(),
        file_name=f"detected_{uploaded_file.name}",
        mime="image/jpeg"
    )

else:
    st.info("👆 Faça upload de uma imagem para começar!")

# Footer
st.markdown("---")
st.markdown("**Desenvolvido com ❤️ usando YOLOv8 e Streamlit**")
```

### 5.3 Executar Streamlit

```bash
streamlit run app.py
```

---

## 6. Fine-tuning do Modelo

### 6.1 Preparar Dataset Customizado

```yaml
# data.yaml
train: /path/to/train/images
val: /path/to/val/images

nc: 1  # Número de classes
names: ['cattle']  # Nome das classes
```

### 6.2 Script de Treinamento

```python
# train.py
from ultralytics import YOLO

# Carrega modelo pré-treinado
model = YOLO('yolov8n.pt')

# Treina
results = model.train(
    data='data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='cattle_model',
    patience=20,
    save=True,
    device=0  # GPU (use 'cpu' para CPU)
)

# Valida
metrics = model.val()

# Exporta
model.export(format='onnx')
```

---

## 7. Batch Processing Paralelo

### 7.1 Processamento com ThreadPoolExecutor

```python
# parallel_processing.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from detect_cattle import CattleDetector
import time

def process_single_image(detector, image_path, output_dir):
    """Processa uma única imagem"""
    try:
        processed_img, count, detections = detector.detect_in_image(str(image_path))
        if processed_img is not None:
            output_path = Path(output_dir) / f"detected_{image_path.name}"
            import cv2
            cv2.imwrite(str(output_path), processed_img)
            return image_path.name, count, True
    except Exception as e:
        return image_path.name, 0, False
    return image_path.name, 0, False

def parallel_process(input_dir, output_dir, max_workers=4):
    """
    Processa imagens em paralelo.
    """
    detector = CattleDetector()
    Path(output_dir).mkdir(exist_ok=True)
    
    # Lista imagens
    image_files = list(Path(input_dir).glob('*.jpg')) + \
                  list(Path(input_dir).glob('*.jpeg')) + \
                  list(Path(input_dir).glob('*.png'))
    
    print(f"🚀 Processando {len(image_files)} imagens com {max_workers} workers")
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submete todas as tarefas
        futures = {
            executor.submit(process_single_image, detector, img, output_dir): img
            for img in image_files
        }
        
        # Processa conforme completam
        for future in as_completed(futures):
            name, count, success = future.result()
            results.append((name, count, success))
            print(f"  ✅ {name}: {count} bovinos")
    
    elapsed = time.time() - start_time
    total_cattle = sum(count for _, count, _ in results)
    
    print(f"\n📊 RESUMO:")
    print(f"  ⏱️  Tempo total: {elapsed:.2f}s")
    print(f"  🐄 Total de gado: {total_cattle}")
    print(f"  📈 Imagens/segundo: {len(image_files)/elapsed:.2f}")

if __name__ == "__main__":
    parallel_process('images', 'output', max_workers=4)
```

---

## 8. Salvar em Diferentes Formatos

### 8.1 Exportar para CSV

```python
# export_csv.py
import csv
from detect_cattle import CattleDetector
from pathlib import Path

detector = CattleDetector()
results = detector.process_directory('images', 'output')

# Salva CSV
with open('output/results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Arquivo', 'Quantidade', 'Detalhes'])
    
    for img in results['images_processed']:
        detections_str = '; '.join([
            f"Conf:{d['confidence']:.2f}" for d in img['detections']
        ])
        writer.writerow([
            img['filename'],
            img['cattle_count'],
            detections_str
        ])

print("✅ CSV salvo em output/results.csv")
```

### 8.2 Exportar para Excel

```python
# export_excel.py
import pandas as pd
from detect_cattle import CattleDetector

detector = CattleDetector()
results = detector.process_directory('images', 'output')

# Cria DataFrame
data = []
for img in results['images_processed']:
    data.append({
        'Arquivo': img['filename'],
        'Quantidade de Gado': img['cattle_count'],
        'Detecções': len(img['detections']),
        'Confiança Média': sum(d['confidence'] for d in img['detections']) / len(img['detections']) if img['detections'] else 0
    })

df = pd.DataFrame(data)

# Salva Excel
df.to_excel('output/results.xlsx', index=False)
print("✅ Excel salvo em output/results.xlsx")
```

---

## 🎓 Exercícios Propostos

### Nível 1: Iniciante
1. Modifique o código para detectar pessoas além de gado
2. Adicione um contador de tempo de processamento por imagem
3. Crie um script que gera um gráfico de barras com a contagem

### Nível 2: Intermediário
1. Implemente o processamento de vídeo (#2)
2. Crie a API REST (#4)
3. Adicione logging detalhado ao sistema

### Nível 3: Avançado
1. Implemente detecção em tempo real (#3)
2. Crie a interface Streamlit (#5)
3. Faça fine-tuning com um dataset customizado (#6)

---

## 📚 Recursos Adicionais

- [Ultralytics Docs](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)

---

**Bons estudos e feliz codificação! 🚀**
