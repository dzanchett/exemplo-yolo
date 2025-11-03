#!/usr/bin/env python3
"""
Script Didático de Contagem de Gado usando YOLOv8
==================================================

Este script demonstra como usar o YOLOv8 para detectar e contar gado (bois) 
em imagens. É projetado para fins educacionais com comentários explicativos.

Autor: Projeto Educacional YOLO
Data: 2025-11-03
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import cv2
from ultralytics import YOLO
import json
from datetime import datetime


class CattleDetector:
    """
    Classe principal para detecção e contagem de gado.
    
    Esta classe encapsula toda a lógica de detecção usando YOLOv8,
    tornando o código mais organizado e reutilizável.
    """
    
    def __init__(self, model_name: str = 'yolov8n.pt', confidence: float = 0.25):
        """
        Inicializa o detector de gado.
        
        Args:
            model_name: Nome do modelo YOLO a ser usado (yolov8n.pt, yolov8s.pt, etc.)
            confidence: Limiar de confiança para detecções (0.0 a 1.0)
        """
        print(f"📦 Carregando modelo YOLO: {model_name}")
        print(f"   Confiança mínima: {confidence}")
        
        # Carrega o modelo YOLO pré-treinado
        # O modelo será baixado automaticamente na primeira execução
        self.model = YOLO(model_name)
        self.confidence = confidence
        
        # Classes relacionadas a gado no dataset COCO
        # 19 = 'cow' (vaca/boi)
        # 20 = 'elephant' (removemos, queremos apenas bovinos)
        # 21 = 'bear' (removemos)
        self.target_classes = [19]  # Apenas 'cow' (bovinos)
        
        print("✅ Modelo carregado com sucesso!")
    
    def detect_in_image(self, image_path: str) -> Tuple[any, int, List]:
        """
        Detecta gado em uma única imagem.
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Tupla contendo (imagem_processada, contagem, lista_de_detecções)
        """
        print(f"\n🔍 Processando: {Path(image_path).name}")
        
        # Lê a imagem usando OpenCV
        image = cv2.imread(image_path)
        if image is None:
            print(f"   ⚠️  Erro ao ler imagem: {image_path}")
            return None, 0, []
        
        # Executa a inferência do YOLO
        # verbose=False para não poluir o output
        results = self.model(image, conf=self.confidence, verbose=False)
        
        # Processa os resultados
        detections = []
        cattle_count = 0
        
        # results[0] contém as detecções da primeira (e única) imagem
        for result in results[0].boxes:
            # Extrai informações de cada detecção
            class_id = int(result.cls[0])  # ID da classe detectada
            confidence = float(result.conf[0])  # Confiança da detecção
            bbox = result.xyxy[0].cpu().numpy()  # Bounding box [x1, y1, x2, y2]
            
            # Verifica se é uma das classes alvo (bovinos)
            if class_id in self.target_classes:
                cattle_count += 1
                
                # Armazena informações da detecção
                detections.append({
                    'class': self.model.names[class_id],
                    'confidence': confidence,
                    'bbox': bbox.tolist()
                })
                
                # Desenha o retângulo na imagem
                x1, y1, x2, y2 = map(int, bbox)
                
                # Cor verde para o retângulo (BGR no OpenCV)
                color = (0, 255, 0)
                thickness = 3
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                
                # Adiciona texto com a classe e confiança
                label = f"{self.model.names[class_id]} {confidence:.2f}"
                
                # Fundo para o texto (para melhor legibilidade)
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                )
                cv2.rectangle(
                    image, 
                    (x1, y1 - text_height - 10), 
                    (x1 + text_width, y1), 
                    color, 
                    -1  # Preenchido
                )
                
                # Texto em branco sobre o fundo verde
                cv2.putText(
                    image, 
                    label, 
                    (x1, y1 - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (255, 255, 255),  # Branco
                    2
                )
        
        print(f"   🐄 Gado detectado: {cattle_count}")
        
        return image, cattle_count, detections
    
    def process_directory(self, input_dir: str, output_dir: str) -> Dict:
        """
        Processa todas as imagens em um diretório.
        
        Args:
            input_dir: Diretório com imagens de entrada
            output_dir: Diretório para salvar resultados
            
        Returns:
            Dicionário com estatísticas do processamento
        """
        print(f"\n{'='*60}")
        print(f"🚀 INICIANDO PROCESSAMENTO DE IMAGENS")
        print(f"{'='*60}")
        print(f"📁 Diretório de entrada: {input_dir}")
        print(f"📁 Diretório de saída: {output_dir}")
        
        # Cria o diretório de saída se não existir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Extensões de imagem suportadas
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        
        # Lista todas as imagens no diretório
        image_files = [
            f for f in Path(input_dir).iterdir()
            if f.suffix.lower() in image_extensions
        ]
        
        if not image_files:
            print("⚠️  Nenhuma imagem encontrada no diretório!")
            return {}
        
        print(f"📸 Total de imagens encontradas: {len(image_files)}")
        
        # Estatísticas
        results = {
            'total_images': len(image_files),
            'total_cattle': 0,
            'images_processed': [],
            'processing_time': None
        }
        
        start_time = datetime.now()
        
        # Processa cada imagem
        for img_file in image_files:
            processed_image, count, detections = self.detect_in_image(str(img_file))
            
            if processed_image is not None:
                # Salva a imagem processada
                output_path = Path(output_dir) / f"detected_{img_file.name}"
                cv2.imwrite(str(output_path), processed_image)
                
                # Atualiza estatísticas
                results['total_cattle'] += count
                results['images_processed'].append({
                    'filename': img_file.name,
                    'cattle_count': count,
                    'detections': detections,
                    'output_path': str(output_path)
                })
        
        end_time = datetime.now()
        results['processing_time'] = (end_time - start_time).total_seconds()
        
        return results
    
    def save_report(self, results: Dict, output_path: str):
        """
        Salva um relatório JSON com os resultados.
        
        Args:
            results: Dicionário com resultados do processamento
            output_path: Caminho para salvar o relatório
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Relatório salvo em: {output_path}")


def print_summary(results: Dict):
    """
    Imprime um resumo dos resultados no console.
    
    Args:
        results: Dicionário com resultados do processamento
    """
    print(f"\n{'='*60}")
    print(f"📊 RESUMO DOS RESULTADOS")
    print(f"{'='*60}")
    print(f"🖼️  Total de imagens processadas: {results['total_images']}")
    print(f"🐄 Total de gado detectado: {results['total_cattle']}")
    print(f"⏱️  Tempo de processamento: {results['processing_time']:.2f} segundos")
    print(f"\n{'='*60}")
    print(f"📋 DETALHES POR IMAGEM:")
    print(f"{'='*60}")
    
    for img_result in results['images_processed']:
        print(f"  • {img_result['filename']}: {img_result['cattle_count']} boi(s)")
    
    print(f"{'='*60}\n")


def main():
    """
    Função principal do script.
    """
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   🐄 Sistema de Detecção e Contagem de Gado - YOLOv8   ║
    ║              Projeto Educacional                         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Configurações
    INPUT_DIR = '/workspace/images'
    OUTPUT_DIR = '/workspace/output'
    REPORT_PATH = '/workspace/output/report.json'
    
    # Parâmetros do modelo
    MODEL_NAME = 'yolov8n.pt'  # yolov8n = nano (mais rápido, menos preciso)
                                 # yolov8s = small
                                 # yolov8m = medium
                                 # yolov8l = large
                                 # yolov8x = extra large (mais lento, mais preciso)
    
    CONFIDENCE_THRESHOLD = 0.25  # Confiança mínima (0.0 a 1.0)
    
    try:
        # Inicializa o detector
        detector = CattleDetector(
            model_name=MODEL_NAME,
            confidence=CONFIDENCE_THRESHOLD
        )
        
        # Processa todas as imagens
        results = detector.process_directory(INPUT_DIR, OUTPUT_DIR)
        
        if results:
            # Salva relatório
            detector.save_report(results, REPORT_PATH)
            
            # Imprime resumo
            print_summary(results)
            
            print("✅ Processamento concluído com sucesso!")
            print(f"📁 Imagens processadas salvas em: {OUTPUT_DIR}")
        else:
            print("❌ Nenhum resultado para processar.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erro durante o processamento: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
