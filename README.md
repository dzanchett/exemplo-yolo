# Projeto Didatico: Contagem de Bois com YOLO

Este repositorio demonstra, passo a passo, como montar um pipeline completo de Visao Computacional para contar bois em imagens utilizando a familia YOLO (especialmente YOLOv8 via a biblioteca `ultralytics`). O foco e ser didatico para fins de ensino, sem a necessidade de atingir a melhor acuracia possivel.

## Visao Geral do Projeto

- `src/train.py` - realiza o treinamento/fine-tuning de um modelo YOLO em um conjunto anotado.
- `src/infer.py` - executa inferencias em imagens ou videos, gera as imagens anotadas e um relatorio CSV com a contagem de animais.
- `src/evaluate.py` - compara as contagens previstas com a contagem manual e calcula metricas simples (MAE, MAPE).
- `configs/cattle.yaml` - arquivo de configuracao do dataset no formato YOLO.
- `data/ground_truth_counts.csv` - modelo de planilha para registrar a contagem manual e validar o pipeline.
- `Dockerfile` - containeriza todo o ambiente para garantir reprodutibilidade.

```
workspace/
|-- configs/
|   `-- cattle.yaml
|-- data/
|   `-- ground_truth_counts.csv
|-- images/
|   |-- img1.jpg
|   |-- img2.jpg
|   |-- img3.jpg
|   `-- img4.jpeg
|-- outputs/
|-- src/
|   |-- __init__.py
|   |-- evaluate.py
|   |-- infer.py
|   `-- train.py
|-- Dockerfile
|-- README.md
`-- requirements.txt
```

## Preparando o Ambiente com Docker

1. Crie a imagem Docker:
   ```bash
   docker build -t yolo-cattle-counter .
   ```
2. Inicie um container montando o diretorio atual para salvar resultados:
   ```bash
   docker run --rm -it -v "$(pwd)":/workspace yolo-cattle-counter
   ```
3. Dentro do container voce ja estara no diretorio `/workspace` com todas as dependencias instaladas. O prompt exibira uma dica para rodar a inferencia.

### Execucao local (sem Docker)

Caso prefira executar localmente:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Preparando o Dataset (Treinamento)

O YOLO espera o seguinte layout dentro de `data/cattle/`:

```
data/cattle/
|-- train/
|   |-- images/
|   `-- labels/
|-- val/
|   |-- images/
|   `-- labels/
`-- test/
    |-- images/
    `-- labels/
```

- As anotacoes devem seguir o formato TXT do YOLO (classe x_center y_center width height, todos normalizados entre 0 e 1).
- Para uma demonstracao em sala, um conjunto pequeno (por exemplo, 20-30 imagens) ja e suficiente. O proprio Ultralytics oferece o dataset `coco128`; basta filtrar a classe `cow` para um exercicio rapido.
- Ajuste os caminhos em `configs/cattle.yaml` caso organize os dados de outra forma.

## Treinamento / Fine-Tuning

Dentro do container (ou no ambiente local com virtualenv), execute:

```bash
python src/train.py --data-config configs/cattle.yaml --epochs 50 --batch-size 16
```

Argumentos uteis:

- `--model`: ponto de partida. Pode ser `yolov8n.pt` (rapido) ou outro checkpoint customizado.
- `--epochs`, `--batch-size`, `--img-size`, `--learning-rate`: hiperparametros que voce consegue adaptar conforme o hardware.
- `--project` e `--run-name`: definem onde os artefatos (pesos, metricas, plots) serao salvos.

Ao final, observe o diretorio `outputs/training_runs/<run-name>/` para encontrar `best.pt`, `results.csv` e graficos de loss.

## Inferencia e Contagem de Bois

Use o modelo pre-treinado no COCO (classe `cow`) ou um checkpoint fine-tunado:

```bash
python src/infer.py   --model yolov8n.pt   --source images   --save-dir outputs/inference_demo
```

O script gera tres tipos de saida dentro de `--save-dir`:

- Imagens/videos anotados com bounding boxes (`predictions/`).
- Arquivos TXT brutos com as deteccoes (uteis para auditoria).
- `cattle_count_report.csv` com a contagem por arquivo e o total geral.

Para usar um checkpoint customizado (por exemplo, o melhor modelo apos o treinamento), ajuste `--model outputs/training_runs/cattle_detection/weights/best.pt`.

## Avaliando a Qualidade da Contagem

1. Abra `data/ground_truth_counts.csv` e preencha a coluna `cattle_count` com a contagem manual para cada imagem.
2. Depois de rodar a inferencia, execute:
   ```bash
   python src/evaluate.py      --predictions outputs/inference_demo/cattle_count_report.csv      --ground-truth data/ground_truth_counts.csv
   ```
3. O script mostra, para cada imagem, a contagem prevista versus a real, alem das metricas agregadas (MAE e MAPE). Isso facilita discutir erros, falsos positivos/negativos e possiveis melhorias.

## Boas Praticas e Extensoes Pedagogicas

- **Qualidade do dataset**: destaque em aula a importancia de anotacoes consistentes (classes, bounding boxes bem ajustados, diversidade de cenarios).
- **Aumentos de dados (data augmentation)**: o YOLO aplica alguns aumentos por padrao, mas voce pode experimentar parametros extra via `model.train(augment=True, ...)`.
- **Transfer learning**: compare iniciar com `yolov8n.pt` com treinar do zero para discutir os ganhos de modelos pre-treinados.
- **Limiares de confianca**: demonstre como `--conf` e `--iou` impactam a contagem final (maior confianca reduz falsos positivos, mas pode perder animais mais dificeis).
- **Desdobramentos**: extensao para videos (contagem frame a frame), integracao com drones, uso de mapas de densidade etc.

## Proximos Passos

- Avalie a necessidade de melhorar a anotacao das imagens ja fornecidas em `images/`.
- Experimente diferentes checkpoints (`yolov8s.pt`, `yolov8m.pt`) e compare tempo de inferencia versus qualidade.
- Gere um notebook Jupyter com exemplos visuais de metricas e deteccoes para uso em sala. O Dockerfile ja contem todas as dependencias do YOLO; instale `jupyter` dentro do container caso queira essa extensao.

Bom aprendizado e bons experimentos!
