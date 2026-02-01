# 🤗 Como Configurar o Modelo no Hugging Face

## Passo 1: Fazer Upload do Modelo

### Opção A: Via Interface Web (mais fácil)

1. **Vai a** https://huggingface.co/new
2. **Cria um novo repositório:**
   - Repository name: `blood-cell-detector` (ou outro nome)
   - License: MIT
   - Visibility: Public (ou Private)
3. **Clica em "Create repository"**
4. **Clica em "Files" → "Add file" → "Upload files"**
5. **Arrasta o `best.pt`** e faz upload
6. **Commit** as mudanças

### Opção B: Via Git (avançado)

```bash
# 1. Instalar git-lfs
git lfs install

# 2. Clonar o repo
git clone https://huggingface.co/SEU-USERNAME/blood-cell-detector

# 3. Copiar modelo
cd blood-cell-detector
cp /caminho/para/best.pt .

# 4. Commit e push
git lfs track "*.pt"
git add best.pt .gitattributes
git commit -m "Add YOLO model"
git push
```

## Passo 2: Obter o URL do Modelo

Depois do upload, o URL será:

```
https://huggingface.co/SEU-USERNAME/SEU-REPO/resolve/main/best.pt
```

**Exemplo:**
```
https://huggingface.co/joaosilva/blood-cell-detector/resolve/main/best.pt
```

## Passo 3: Configurar no Código

### Opção A: Editar `app.py` diretamente

Abre `app.py` e na linha ~30, substitui:

```python
HUGGING_FACE_MODEL_URL = os.getenv(
    "HUGGING_FACE_MODEL_URL",
    "https://huggingface.co/SEU-USERNAME/SEU-REPO/resolve/main/best.pt"  # <-- AQUI
)
```

### Opção B: Usar Streamlit Secrets (recomendado para deploy)

1. **No Streamlit Cloud**, vai a "Settings" → "Secrets"
2. **Adiciona:**

```toml
HUGGING_FACE_MODEL_URL = "https://huggingface.co/SEU-USERNAME/SEU-REPO/resolve/main/best.pt"
```

3. **Salva**

### Opção C: Variável de ambiente local

```bash
# Windows (PowerShell)
$env:HUGGING_FACE_MODEL_URL="https://huggingface.co/SEU-USERNAME/SEU-REPO/resolve/main/best.pt"

# macOS/Linux
export HUGGING_FACE_MODEL_URL="https://huggingface.co/SEU-USERNAME/SEU-REPO/resolve/main/best.pt"
```

## Passo 4: Testar

### Localmente:

```bash
streamlit run app.py
```

A primeira vez vai fazer download do modelo (1-2 min).

### No Streamlit Cloud:

```bash
git add app.py requirements.txt
git commit -m "Add Hugging Face model download"
git push
```

Aguarda o redeploy automático.

## ⚠️ Notas Importantes

### Repositório Privado

Se o teu repo do Hugging Face for **privado**, precisas de token:

1. **Gera um token** em: https://huggingface.co/settings/tokens
2. **Adiciona ao código:**

```python
# Em app.py, na função download_model_from_huggingface:
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
response = requests.get(url, stream=True, headers=headers)
```

3. **Adiciona HF_TOKEN aos Secrets** no Streamlit Cloud

### Modelo Grande (>500MB)

- Hugging Face suporta ficheiros grandes (até 50GB)
- O download pode demorar 2-5 minutos na primeira vez
- Depois fica em cache

### Verificar Download

Para ver o progresso no Streamlit Cloud:
1. Vai a "Manage app" → "Logs"
2. Vê a mensagem "A fazer download do modelo..."

## 🎯 Vantagens vs GitHub

| Aspeto | GitHub | Hugging Face |
|--------|--------|--------------|
| Limite ficheiro | 100MB (sem LFS) | 50GB |
| Git LFS necessário | Sim (>100MB) | Não |
| CDN global | Não | Sim (mais rápido) |
| Específico ML | Não | Sim |
| Download direto | Complicado | Simples |

## ✅ Checklist Final

- [ ] Modelo uploadado no Hugging Face
- [ ] URL copiado
- [ ] `app.py` atualizado com URL correto
- [ ] `requirements.txt` tem `requests>=2.31.0`
- [ ] Testado localmente
- [ ] Push para GitHub
- [ ] Verificar logs no Streamlit Cloud

---

**Pronto!** 🎉 Agora o modelo é carregado automaticamente do Hugging Face sempre que a app inicia.
