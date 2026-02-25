# Blood Cell Detector (Streamlit)

Aplicação web em **Streamlit** para **deteção e contagem de células sanguíneas** em imagens de microscopia (ex.: RBC, WBC e plaquetas), com opção de **classificação de subtipos de WBC** (quando ativada no interface).

> ⚠️ **Aviso / Isenção de responsabilidade**  
> Este projeto é **académico/demonstração**. **Não** é um dispositivo médico e **não** deve ser usado para decisões clínicas.

---

## Demo (Streamlit Cloud)
A app está disponível em:  
https://blood-cell-detector.streamlit.app

---

## Funcionalidades (alto nível)
- Upload de imagens (microscopia de sangue periférico)
- Deteção por *bounding boxes* (pipeline YOLO)
- Contagem por classe (RBC / WBC / Platelets)
- Ajuste de **confidence threshold** (e/ou parâmetros no UI, consoante a versão)
- (Opcional) Classificação de **subtipos de WBC** em recortes (quando ativado)
- Páginas extra via `pages/` (Streamlit multipage)

---

## Estrutura do repositório

```
.
├─ app.py                # Entry-point da Streamlit app
├─ pages/                # Páginas adicionais (Streamlit multipage)
├─ examples/             # Imagens de exemplo / inputs para demo
├─ images/               # Imagens estáticas (ex.: fotos da equipa, UI assets)
├─ requirements.txt      # Dependências Python
├─ packages.txt          # Dependências do sistema (para deploy, ex.: OpenCV)
└─ .gitignore
```

---

## Como correr localmente

### 1) Pré-requisitos
- Python 3.10+ (recomendado)
- `pip` / `venv`

### 2) Criar ambiente virtual e instalar dependências
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Executar a app
```bash
streamlit run app.py
```

A app deverá abrir no browser (por defeito em `http://localhost:8501`).

---

## Deploy no Streamlit Community Cloud
1. Faz push do repositório para o GitHub.
2. No Streamlit Cloud, escolhe:
   - **Repository**: o teu repo
   - **Branch**: `main` (ou outro)
   - **Main file path**: `app.py`

### Nota sobre `packages.txt`
Se estiveres a usar OpenCV (ou libs que dependem de pacotes do sistema), o Streamlit Cloud pode precisar do `packages.txt`.  
Mantém esse ficheiro na root do repo e inclui lá as dependências do sistema necessárias (ex.: libs para `opencv-python`).

---

## Utilização (na app)
1. Faz upload de uma imagem de microscopia.
2. Seleciona o modelo (se houver lista de modelos no UI).
3. Ajusta o **confidence threshold** conforme necessário:
   - **mais alto** → menos deteções (menos falsos positivos)
   - **mais baixo** → mais deteções (mais sensível, mas pode aumentar falsos positivos)
4. Visualiza caixas + contagem por classe.
5. (Opcional) ativa classificação de WBC (se disponível) para obter subtipos.

---

## Troubleshooting

### Erros com OpenCV no deploy
- Confirma que `requirements.txt` inclui a dependência correta (ex.: `opencv-python` ou `opencv-python-headless`).
- Se o ambiente precisar de libs do sistema, adiciona-as ao `packages.txt`.

### “Module not found”
- Garante que instalaste o `requirements.txt` no ambiente virtual ativo.
- Se adicionaste novas dependências, atualiza `requirements.txt`.

---

## Contribuidores
- Diogo Casquinha  
- Vicente Soares  
- Guilherme Pereira  
- Gabriel Afonso  

Supervisor: Simão Gonçalves  
Instituição: NOVA Executive Education & Samsung

---

## Licença
Define a licença conforme a entrega do projeto (ex.: MIT, Apache-2.0, ou “All rights reserved”).  
Se ainda não tens, podes criar um ficheiro `LICENSE` e escolher uma licença apropriada.
