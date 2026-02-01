# 📦 Models Directory

Esta pasta contém os modelos YOLO treinados para deteção de células sanguíneas.

## 📥 Como Adicionar o Modelo

1. **Coloca o teu ficheiro de weights aqui**

   ```
   models/
   └── best.pt    # <-- Nome padrão esperado
   ```

2. **Nomes de ficheiros suportados:**
   - `best.pt` (padrão)
   - Qualquer `.pt` (configurável via `MODEL_PATH`)

## ⚙️ Configuração

### Usar nome diferente

Se o teu modelo tiver outro nome (ex: `blood_cell_model.pt`):

**Opção 1: Variável de ambiente**

```bash
# Windows (PowerShell)
$env:MODEL_PATH="models/blood_cell_model.pt"

# Windows (CMD)
set MODEL_PATH=models/blood_cell_model.pt

# macOS/Linux
export MODEL_PATH=models/blood_cell_model.pt
```

**Opção 2: Editar app.py**

```python
# Em app.py, linha ~30
MODEL_PATH = "models/blood_cell_model.pt"  # Alterar aqui
```

### Usar modelo de outro local

```bash
# Exemplo: modelo na pasta raiz
export MODEL_PATH="my_model.pt"

# Exemplo: caminho absoluto
export MODEL_PATH="/home/user/models/blood_cells.pt"
```

## 🎯 Requisitos do Modelo

### Classes Esperadas

O modelo deve estar treinado para detetar **3 classes**:

1. **RBC** - Red Blood Cells (Glóbulos Vermelhos)
2. **WBC** - White Blood Cells (Glóbulos Brancos)  
3. **Platelets** - Plaquetas

### Formato

- **Tipo**: YOLO v8/v5 (Ultralytics)
- **Extensão**: `.pt` (PyTorch)
- **Framework**: Ultralytics YOLO

### Como Verificar as Classes do Modelo

```python
from ultralytics import YOLO

model = YOLO('models/best.pt')
print(model.names)  # Deve mostrar: {0: 'RBC', 1: 'WBC', 2: 'Platelets'}
```

## 🔄 Mapeamento de Classes

Se o teu modelo usar **nomes diferentes**, podes mapeá-los sem retreinar:

**Edita:** `src/infer.py`, função `map_class_name()`

```python
mapping = {
    # Teus nomes -> Nomes standard
    "red_blood_cell": "RBC",
    "white_blood_cell": "WBC",
    "platelet": "Platelets",
    
    # Ou outros exemplos:
    "eritrocito": "RBC",
    "leucocito": "WBC",
    "plaqueta": "Platelets",
}
```

## 📊 Performance do Modelo

Para melhor performance:

- **Resolução recomendada**: 640x640 pixels
- **Confidence threshold**: 0.25-0.5 (ajustável na app)
- **IOU threshold**: 0.45 (ajustável na app)

### Otimizar Modelo

```python
# Exportar para ONNX (mais rápido em CPU)
from ultralytics import YOLO

model = YOLO('models/best.pt')
model.export(format='onnx')  # Cria best.onnx
```

Depois alterar em `app.py`:
```python
MODEL_PATH = "models/best.onnx"
```

## 🚫 .gitignore

Por defeito, ficheiros `.pt` **NÃO** são versionados no Git (são grandes).

### Para Versionar Modelos

Se quiseres versionar o modelo no GitHub:

1. **Remove `*.pt` do `.gitignore`**
2. **Usa Git LFS** (Large File Storage):

```bash
git lfs install
git lfs track "*.pt"
git add .gitattributes
git add models/best.pt
git commit -m "Add trained model"
git push
```

### Alternativas ao Git LFS

- **Google Drive / Dropbox**: Partilha link e documenta no README
- **Hugging Face Hub**: Upload do modelo
- **GitHub Releases**: Anexar como binary

## 📝 Exemplo de Treino

Se ainda não tens modelo, podes treinar usando Ultralytics:

```python
from ultralytics import YOLO

# Carregar modelo base
model = YOLO('yolov8n.pt')  # nano (rápido) ou yolov8s.pt (mais preciso)

# Treinar
model.train(
    data='blood_cells.yaml',  # Ficheiro de configuração do dataset
    epochs=100,
    imgsz=640,
    batch=16,
    name='blood_cell_detector'
)

# Modelo treinado ficará em: runs/detect/blood_cell_detector/weights/best.pt
# Copia para: models/best.pt
```

### Estrutura do dataset (blood_cells.yaml)

```yaml
path: /path/to/dataset
train: images/train
val: images/val

names:
  0: RBC
  1: WBC
  2: Platelets
```

## ❓ Troubleshooting

### Erro: "Model not found"

✅ **Solução**: Verifica se `best.pt` existe em `models/`

### Erro: "No module named 'ultralytics'"

✅ **Solução**: `pip install ultralytics`

### Modelo muito lento

✅ **Soluções**:
- Usa modelo menor (yolov8n.pt vs yolov8x.pt)
- Exporta para ONNX
- Usa GPU (se disponível)

### Classes erradas detetadas

✅ **Solução**: Configura mapeamento em `src/infer.py`

---

**Nota**: Este ficheiro é apenas informativo. Podes deletá-lo após configurar o modelo.
