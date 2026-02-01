# 🔬 Blood Cell Detection System

Aplicação web para deteção automática de células sanguíneas (RBC, WBC, Platelets) usando YOLO + Streamlit.

## 📋 Características

- ✅ Upload de múltiplas imagens
- ✅ Deteção automática com YOLO (Ultralytics)
- ✅ Visualização lado-a-lado (original vs anotada)
- ✅ Métricas por imagem e agregadas
- ✅ Download de resultados (CSV + ZIP)
- ✅ Interface minimalista e responsiva
- ✅ Análise extra desbloqueável (>50 imagens)

## 🚀 Quick Start

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd blood_cell_detector
```

### 2. Criar Virtual Environment (VSCode)

**Opção A: Via Terminal Integrado do VSCode**

```bash
# No terminal do VSCode
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (macOS/Linux)
source venv/bin/activate
```

**Opção B: Via Command Palette do VSCode**

1. Pressiona `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (macOS)
2. Escreve: `Python: Create Environment`
3. Escolhe `Venv`
4. Seleciona o interpretador Python desejado
5. VSCode criará e ativará automaticamente

### 3. Instalar Dependências

```bash
# Com venv ativado
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota:** Se tiveres GPU NVIDIA, instala PyTorch com suporte CUDA:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 4. Adicionar o Modelo YOLO

Coloca o teu ficheiro de weights (`best.pt`) na pasta `models/`:

```
blood_cell_detector/
├── models/
│   └── best.pt          # <-- Coloca aqui o teu modelo
├── src/
├── app.py
└── ...
```

**Nota:** Se o teu modelo tiver outro nome ou estiver noutro local, podes configurar via variável de ambiente:

```bash
# Windows
set MODEL_PATH=path/to/your/model.pt

# macOS/Linux
export MODEL_PATH=path/to/your/model.pt
```

### 5. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no browser em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
blood_cell_detector/
│
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências Python
├── README.md                   # Este ficheiro
├── .gitignore                  # Ficheiros a ignorar no Git
│
├── src/                        # Código fonte
│   ├── __init__.py
│   ├── infer.py               # Lógica de inferência YOLO
│   └── io_utils.py            # Utilitários I/O (zip, csv, etc.)
│
└── models/                     # Modelos YOLO
    ├── best.pt                # Teu modelo treinado
    └── README.md              # Instruções sobre modelos
```

## 🎯 Como Usar

### Interface Principal

1. **Upload de Imagens**
   - Clica em "Browse files" ou arrasta imagens
   - Formatos suportados: JPG, JPEG, PNG
   - Suporta upload múltiplo

2. **Configurações (Sidebar)**
   - **Confidence Threshold**: Ajusta confiança mínima (padrão: 0.25)
   - **IOU Threshold**: Ajusta NMS (padrão: 0.45)
   - **Mostrar labels**: Toggle para labels nas boxes
   - **Mostrar confidence**: Toggle para valores de confiança

3. **Executar Deteção**
   - Clica em "Run Detection"
   - Aguarda processamento (barra de progresso)

4. **Visualizar Resultados**
   - Cada imagem mostra original vs anotada
   - Métricas individuais (contagens e percentagens)
   - Resumo agregado do batch
   - Tabela detalhada com todos os resultados

5. **Download**
   - **CSV**: Tabela com todas as métricas
   - **ZIP**: Todas as imagens anotadas

### Análise Extra (>50 imagens)

Quando processares **mais de 50 imagens**, uma nova secção é desbloqueada:

- Comparação com valores de referência (configuráveis)
- Input de dados do utilizador (idade, sexo, peso)
- **IMPORTANTE**: Inclui disclaimers fortes sobre não ser ferramenta clínica

⚠️ **Aviso**: Esta funcionalidade é apenas para demonstração educacional e não tem valor clínico.

## ⚙️ Configuração do Modelo

### Classes Esperadas

O modelo deve estar treinado para detetar:
- `RBC` (Red Blood Cells / Glóbulos Vermelhos)
- `WBC` (White Blood Cells / Glóbulos Brancos)
- `Platelets` (Plaquetas)

### Mapeamento de Classes

Se o teu modelo usar nomes diferentes, podes editá-los em `src/infer.py`:

```python
# Em src/infer.py, função map_class_name()
mapping = {
    "red_blood_cell": "RBC",      # Exemplo
    "white_blood_cell": "WBC",    # Exemplo
    "platelet": "Platelets",      # Exemplo
}
```

### Valores de Referência (Análise Extra)

Para personalizar os valores de referência na análise extra, edita em `app.py`:

```python
# Em app.py, procura por reference_ranges
reference_ranges = {
    "RBC": {"min": 40.0, "max": 55.0, "unit": "%"},
    "WBC": {"min": 0.5, "max": 2.0, "unit": "%"},
    "Platelets": {"min": 15.0, "max": 40.0, "unit": "%"},
}
```

## 🐙 Git & GitHub

### Inicializar Repositório Local

```bash
git init
git add .
git commit -m "Initial commit: Blood Cell Detection App"
```

### Conectar ao GitHub

1. Cria um repositório no GitHub (vazio, sem README)
2. Conecta o repositório local:

```bash
git remote add origin https://github.com/seu-username/blood-cell-detector.git
git branch -M main
git push -u origin main
```

### Workflow Recomendado

```bash
# Fazer alterações
git add .
git commit -m "Descrição das alterações"
git push
```

### Versionar Modelos (Opcional)

Por defeito, ficheiros `.pt` estão no `.gitignore` (são grandes). Se quiseres versioná-los:

1. Remove `*.pt` do `.gitignore`
2. Usa Git LFS para ficheiros grandes:

```bash
git lfs install
git lfs track "*.pt"
git add .gitattributes
git commit -m "Add Git LFS tracking for models"
```

## 🛠️ Desenvolvimento

### Adicionar Novas Features

1. Cria um branch:
```bash
git checkout -b feature/nova-feature
```

2. Desenvolve e testa

3. Commit e push:
```bash
git add .
git commit -m "Add: nova feature"
git push origin feature/nova-feature
```

4. Cria Pull Request no GitHub

### Debugging

Para debug, podes usar:

```python
# Em qualquer ficheiro
import streamlit as st

# Mostrar variáveis
st.write(variavel)
st.json(dicionario)

# Logs no terminal
print(f"Debug: {valor}")
```

### Testes

Para testar funções individuais:

```python
# Exemplo: testar load_model
from src.infer import load_model

model = load_model("models/best.pt")
print(f"Modelo carregado: {model.names}")
```

## 📊 Performance

### Otimizações Implementadas

- ✅ Model caching (`@st.cache_resource`)
- ✅ Processamento batch eficiente
- ✅ Conversões de imagem otimizadas

### GPU vs CPU

- **CPU**: Funciona out-of-the-box
- **GPU**: ~10-50x mais rápido (depende do modelo)

Para usar GPU, certifica-te que tens:
1. GPU NVIDIA compatível
2. CUDA instalado
3. PyTorch com CUDA (ver instruções acima)

### Limites Recomendados

- **Imagens por batch**: Até 200 (depende da RAM)
- **Tamanho de imagem**: Até 4K (redimensiona se necessário)
- **Concurrent users**: 1-5 (Streamlit open-source)

## ❓ FAQ

### P: O modelo não é detetado?
**R:** Verifica se `models/best.pt` existe ou define `MODEL_PATH`.

### P: Erro "CUDA out of memory"?
**R:** Reduz o batch size ou usa CPU (comentar `device='cuda'` se existir).

### P: As classes não aparecem corretamente?
**R:** Verifica o mapeamento em `src/infer.py` função `map_class_name()`.

### P: Como fazer deploy na cloud?
**R:** Opções:
- Streamlit Cloud (grátis): https://streamlit.io/cloud
- Heroku (requer config extra)
- AWS/GCP/Azure (mais complexo)

### P: Posso usar outro formato de modelo?
**R:** Sim, desde que seja compatível com Ultralytics YOLO (.pt, .onnx, etc.)

## 📝 Notas Importantes

### Disclaimers

- ⚠️ Esta app **NÃO** é uma ferramenta de diagnóstico médico
- ⚠️ Resultados são apenas demonstrativos e educacionais
- ⚠️ Consulta sempre um profissional de saúde qualificado

### Privacidade

- ✅ Nenhuma imagem é guardada ou enviada para servidores
- ✅ Processamento 100% local
- ✅ Sem tracking ou analytics

### Licença

Este projeto é open-source. Consulta o ficheiro LICENSE para detalhes.

## 🤝 Contribuir

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Cria um branch (`git checkout -b feature/amazing-feature`)
3. Commit as alterações (`git commit -m 'Add amazing feature'`)
4. Push para o branch (`git push origin feature/amazing-feature`)
5. Abre um Pull Request

## 📞 Suporte

Para questões ou problemas:
- Abre uma Issue no GitHub
- Consulta a documentação do Ultralytics: https://docs.ultralytics.com
- Consulta a documentação do Streamlit: https://docs.streamlit.io

## 🙏 Agradecimentos

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [Streamlit](https://streamlit.io)
- Comunidade open-source

---

**Feito com ❤️ para análise de células sanguíneas**
