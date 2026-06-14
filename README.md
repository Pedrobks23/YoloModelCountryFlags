# 🏴 Detecção de Bandeiras de Países com YOLOv8

Projeto da disciplina de **Ciência de Dados — Projeto 3 (Deep Learning / YOLO)**.

Treinamento e avaliação de um modelo **YOLOv8** para detectar **86 bandeiras nacionais**
em imagens, com aplicação em fotos reais capturadas pelo grupo.

> 🎯 **Classe inédita:** "bandeira de país" **não** faz parte das 80 classes do dataset
> COCO sobre as quais o YOLO é pré-treinado — atendendo ao requisito do enunciado.

---

## 👥 Integrantes

- Pedro Pereira da Silva — matrícula 2013702
- Victor Rios Dantas — matrícula 2310350

---

## 📁 Estrutura do repositório

```
YoloModelCountryFlags/
├── README.md                  # Este arquivo
├── YOLO_Bandeiras.ipynb       # Notebook principal (EXECUTADO no Colab, com saídas)
├── scripts/
│   └── limpar_dataset.py      # Script de limpeza/reindexação do dataset
├── docs/
│   ├── results.png            # Curvas de treinamento (geradas pelo YOLO)
│   ├── confusion_matrix.png   # Matriz de confusão
│   └── inferencias/           # Prints das detecções (fotos reais + teste)
└── data/
    └── LINK_DATASET.md        # Link/instruções p/ baixar o dataset (não versionar o .zip)
```

> 📄 O **relatório técnico (PDF)** é entregue diretamente na tarefa do AVA, conforme o
> enunciado — não precisa estar versionado neste repositório.

> ⚠️ **Não suba o dataset (`.zip`, imagens) para o GitHub** — são ~200 MB. Deixe apenas
> o link do Roboflow e instruções de download.

---

## 📊 Dataset

| | |
|---|---|
| **Origem** | [Roboflow Universe — country-flags-2t33e (v4)](https://universe.roboflow.com/phamdata/country-flags-2t33e/dataset/4) |
| **Licença** | CC BY 4.0 |
| **Classes** | 86 bandeiras (após limpeza) |
| **Imagens** | 10.187 (treino: 8.940 · validação: 827 · teste: 420) |

### Limpeza aplicada

As classes originais `0 (Afghanistan)` e `1 (Albania)` tinham anotações corrompidas e
foram removidas. O script [`scripts/limpar_dataset.py`](scripts/limpar_dataset.py):

- Remove as bounding boxes dessas classes (167 caixas);
- Reindexa as 86 classes restantes (0–85);
- Atualiza o `data.yaml` (`nc: 88 → 86`);
- Gera uma cópia limpa **sem alterar o original**.

---

## 🚀 Como executar

O notebook foi feito para rodar no **Google Colab** (com GPU).

1. **Abra o notebook no Colab:**
   `Arquivo → Abrir notebook → GitHub` e cole a URL deste repositório, ou faça upload de
   `YOLO_Bandeiras.ipynb`.

2. **Ative a GPU:** `Ambiente de execução → Alterar tipo de ambiente → GPU (T4)`.

3. **Execute as células na ordem.** Quando solicitado:
   - **Upload do dataset:** envie o `dataset_clean.zip` (gerado pelo script de limpeza);
   - **Upload das fotos reais:** envie as fotos de bandeiras capturadas pelo grupo.

4. **Treinamento:** 60 épocas, `yolov8s.pt`, `imgsz=640`, `batch=16`.
   Se aparecer `CUDA out of memory`, reduza `batch` para `8`.

### Reproduzir a limpeza do dataset localmente (opcional)

```bash
pip install pyyaml
python scripts/limpar_dataset.py
```

---

## 🧠 Modelo e hiperparâmetros

| Parâmetro | Valor |
|-----------|-------|
| Modelo base | `yolov8s.pt` (small, 11,2 M parâmetros) |
| Épocas | 60 |
| Resolução (`imgsz`) | 640 |
| Batch | 16 |
| Early stopping (`patience`) | 15 |

---

## 📈 Resultados

Métricas obtidas no **conjunto de teste** (420 imagens):

| Métrica | Valor |
|---------|-------|
| Precisão (Precision) | **0,9682** |
| Revocação (Recall) | **0,9642** |
| mAP@0.5 | **0,9844** |
| mAP@0.5:0.95 | **0,9742** |

### Curvas de treinamento e matriz de confusão

![Curvas de treinamento](docs/results.png)

![Matriz de confusão](docs/confusion_matrix.png)

### Inferência em fotos reais (capturadas pelo grupo)

| Bandeira | Predição | Confiança | Resultado |
|----------|----------|-----------|-----------|
| Estados Unidos | United States | 76,2% | ✅ |
| Brasil | Brazil | 73,0% | ✅ |
| Reino Unido | Anguilla Flag | 68,5% | ❌ (classe ausente no dataset) |
| Portugal | Morocco | 65,1% | ❌ (foto distante / cores parecidas) |

![Detecções nas fotos reais](docs/inferencias/fotos_reais.png)

> O alto desempenho no teste (mAP@0.5 = 0,98) contrasta com os erros em fotos reais do
> Reino Unido e Portugal — discutido no relatório como efeito de **classe ausente** e
> **diferença de domínio** (domain gap) entre o dataset e as condições de captura.

---

## 📝 Licença

Dataset sob licença **CC BY 4.0** (Roboflow). Código deste repositório para fins
acadêmicos.
