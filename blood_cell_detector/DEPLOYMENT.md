# 🚀 Deployment Guide - Streamlit Cloud

Este guia mostra como fazer deploy da aplicação no **Streamlit Cloud** (gratuito).

## 📋 Pré-requisitos

- ✅ Conta no [GitHub](https://github.com)
- ✅ Conta no [Streamlit Cloud](https://streamlit.io/cloud)
- ✅ Repositório público no GitHub com a app

## 🔧 Preparação

### 1. Adicionar ficheiro packages.txt (opcional)

Se precisares de dependências do sistema (ex: libgl1 para OpenCV):

```bash
# Criar packages.txt na raiz
echo "libgl1" > packages.txt
```

### 2. Adicionar .streamlit/secrets.toml (se necessário)

Para variáveis de ambiente sensíveis:

```toml
# .streamlit/secrets.toml (NÃO versionar)
MODEL_PATH = "models/best.pt"
```

**Importante**: Adiciona ao `.gitignore`:
```
.streamlit/secrets.toml
```

### 3. Adicionar modelo ao repositório

**Opção A: Git LFS** (recomendado para ficheiros >100MB)

```bash
git lfs install
git lfs track "*.pt"
git add .gitattributes
git add models/best.pt
git commit -m "Add model with Git LFS"
git push
```

**Opção B: GitHub Releases** (se modelo >100MB e sem LFS)

1. Cria um Release no GitHub
2. Anexa o `best.pt` como binary
3. Modifica `app.py` para fazer download:

```python
import requests
from pathlib import Path

MODEL_PATH = "models/best.pt"

# Download se não existir
if not Path(MODEL_PATH).exists():
    url = "https://github.com/USER/REPO/releases/download/v1.0/best.pt"
    Path("models").mkdir(exist_ok=True)
    
    with st.spinner("A fazer download do modelo..."):
        r = requests.get(url)
        with open(MODEL_PATH, 'wb') as f:
            f.write(r.content)
```

**Opção C: Modelo externo** (Google Drive, Hugging Face, etc.)

Semelhante à Opção B, mas com URL do serviço externo.

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Push para GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Passo 2: Aceder ao Streamlit Cloud

1. Vai a https://streamlit.io/cloud
2. Faz login com GitHub
3. Clica em **"New app"**

### Passo 3: Configurar App

Preenche os campos:

- **Repository**: `username/blood-cell-detector`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL** (opcional): `blood-cell-detector` (ou personaliza)

### Passo 4: Advanced Settings (se necessário)

Clica em "Advanced settings" e configura:

- **Python version**: 3.10 (ou a que usaste)
- **Secrets**: Se usares secrets, cola aqui o conteúdo de `.streamlit/secrets.toml`

### Passo 5: Deploy!

Clica em **"Deploy!"**

A app ficará disponível em:
```
https://YOUR-APP-NAME.streamlit.app
```

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError"

✅ **Solução**: Verifica se todos os packages estão em `requirements.txt`

### Erro: "Model file not found"

✅ **Soluções**:
- Verifica se `models/best.pt` foi pushed
- Se usaste Git LFS, verifica se está ativado
- Considera usar download automático (ver Opção B/C acima)

### Erro: "Memory limit exceeded"

✅ **Soluções**:
- Streamlit Cloud tem ~1GB RAM no plano grátis
- Usa modelo menor (yolov8n.pt em vez de yolov8x.pt)
- Limita número de imagens processadas simultaneamente
- Considera upgrade para Streamlit Cloud Pro

### App lenta

✅ **Soluções**:
- Streamlit Cloud usa CPU (não GPU)
- Exporta modelo para ONNX (mais rápido)
- Reduz resolução de inferência
- Usa modelo nano (yolov8n.pt)

### Erro de OpenCV: "libGL.so.1"

✅ **Solução**: Criar `packages.txt` com:
```
libgl1-mesa-glx
```

## 📊 Monitorização

### Ver Logs

No dashboard do Streamlit Cloud:
1. Clica na tua app
2. Clica em "︙" (menu)
3. Seleciona "Logs"

### Reiniciar App

1. No dashboard, clica na app
2. Menu "︙" → "Reboot app"

### Atualizar App

Simplesmente faz push para o GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```

A app redeploy automaticamente!

## 🔒 Privacidade & Segurança

### Dados do Utilizador

- ✅ Imagens processadas localmente (browser do user)
- ✅ Nada é guardado em servidor
- ✅ Privacidade garantida

### Secrets

NUNCA committes:
- API keys
- Passwords
- Tokens
- Dados sensíveis

Usa `.streamlit/secrets.toml` e adiciona ao `.gitignore`.

## 💰 Limites do Plano Grátis

Streamlit Cloud Free Tier:
- ✅ 1 app pública
- ✅ ~1GB RAM
- ✅ CPU partilhada
- ✅ Unlimited viewers
- ❌ Sem GPU

Para mais recursos: https://streamlit.io/cloud#pricing

## 🔄 Alternativas de Deployment

### Heroku

```bash
# Requer: Procfile, runtime.txt
echo "web: streamlit run app.py --server.port=$PORT" > Procfile
echo "python-3.10.0" > runtime.txt
```

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

### AWS/GCP/Azure

Consulta documentação específica de cada cloud provider.

---

## ✅ Checklist Final

Antes de fazer deploy:

- [ ] `requirements.txt` está completo
- [ ] `.gitignore` configurado (sem secrets)
- [ ] Modelo está no repositório ou configurado download
- [ ] App testada localmente (`streamlit run app.py`)
- [ ] README atualizado com URL da app deployed
- [ ] Secrets configurados (se necessário)

---

**Pronto!** 🎉 A tua app está live e acessível para qualquer pessoa!
