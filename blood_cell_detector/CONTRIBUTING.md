# Contributing to Blood Cell Detection System

Obrigado pelo teu interesse em contribuir! 🎉

## 📋 Código de Conduta

- Sê respeitoso e inclusivo
- Aceita críticas construtivas
- Foca no que é melhor para a comunidade
- Mostra empatia com outros contribuidores

## 🚀 Como Contribuir

### Reportar Bugs

Se encontraste um bug:

1. **Verifica** se já foi reportado nas [Issues](https://github.com/USER/REPO/issues)
2. **Abre uma nova Issue** com:
   - Título descritivo
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots (se aplicável)
   - Versão do Python e SO
   - Logs relevantes

**Template de Bug Report:**

```markdown
**Descrição do Bug**
[Descrição clara do problema]

**Passos para Reproduzir**
1. Vai a '...'
2. Clica em '....'
3. Vê erro

**Comportamento Esperado**
[O que deveria acontecer]

**Screenshots**
[Se aplicável]

**Ambiente:**
 - OS: [e.g. Windows 11]
 - Python: [e.g. 3.10.5]
 - Versão da App: [e.g. 1.0.0]

**Informação Adicional**
[Qualquer contexto extra]
```

### Sugerir Features

Para sugerir uma nova funcionalidade:

1. **Verifica** se já foi sugerida
2. **Abre uma Issue** com label `enhancement`
3. **Descreve**:
   - Problema que resolve
   - Solução proposta
   - Alternativas consideradas
   - Mockups/exemplos (se aplicável)

**Template de Feature Request:**

```markdown
**Descrição da Feature**
[Descrição clara da funcionalidade]

**Problema que Resolve**
[Qual o problema/necessidade]

**Solução Proposta**
[Como implementarias]

**Alternativas**
[Outras soluções consideradas]

**Contexto Adicional**
[Screenshots, mockups, etc.]
```

## 💻 Contribuir Código

### Setup do Ambiente de Desenvolvimento

```bash
# 1. Fork o repositório no GitHub

# 2. Clone o teu fork
git clone https://github.com/TEU-USERNAME/blood-cell-detector.git
cd blood-cell-detector

# 3. Adiciona upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/blood-cell-detector.git

# 4. Cria virtual environment
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 5. Instala dependências
pip install -r requirements.txt

# 6. Instala dependências de desenvolvimento (se existirem)
pip install -r requirements-dev.txt  # opcional
```

### Workflow de Desenvolvimento

```bash
# 1. Cria um branch para a tua feature
git checkout -b feature/nome-da-feature

# 2. Faz as alterações

# 3. Testa localmente
python test_setup.py
streamlit run app.py

# 4. Commit com mensagens descritivas
git add .
git commit -m "Add: descrição da alteração"

# 5. Push para o teu fork
git push origin feature/nome-da-feature

# 6. Abre Pull Request no GitHub
```

### Convenções de Código

#### Estilo Python

- Segue [PEP 8](https://pep8.org/)
- Usa **4 espaços** para indentação (não tabs)
- Máximo **88 caracteres** por linha (compatível com Black)
- Usa **type hints** quando possível

```python
def process_image(
    image: np.ndarray, 
    threshold: float = 0.25
) -> Dict[str, Any]:
    """
    Processa uma imagem.
    
    Args:
        image: Imagem em formato numpy array
        threshold: Limiar de confiança
        
    Returns:
        Dicionário com resultados
    """
    pass
```

#### Mensagens de Commit

Usa [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - Nova funcionalidade
- `fix:` - Bug fix
- `docs:` - Documentação
- `style:` - Formatação (não afeta lógica)
- `refactor:` - Refactoring de código
- `test:` - Adicionar/modificar testes
- `chore:` - Manutenção (deps, config, etc.)

**Exemplos:**

```bash
git commit -m "feat: add export to Excel functionality"
git commit -m "fix: resolve memory leak in batch processing"
git commit -m "docs: update README with GPU setup instructions"
git commit -m "refactor: simplify image loading logic"
```

#### Docstrings

Usa Google Style:

```python
def calculate_metrics(results: List[Dict]) -> Dict[str, Any]:
    """
    Calcula métricas agregadas.
    
    Args:
        results: Lista de resultados individuais
        
    Returns:
        Dicionário com métricas agregadas contendo:
            - total_counts: contagens totais por classe
            - percentages: percentagens
            - num_images: número de imagens
            
    Raises:
        ValueError: Se results estiver vazio
        
    Examples:
        >>> results = [{"counts": {"RBC": 10}}]
        >>> metrics = calculate_metrics(results)
        >>> metrics["total_counts"]["RBC"]
        10
    """
    pass
```

### Testes

Antes de submeter PR:

```bash
# 1. Testa setup
python test_setup.py

# 2. Testa a app manualmente
streamlit run app.py

# 3. Testa batch processing (se aplicável)
python batch_process.py --input test_images --output test_output --save-csv

# 4. Verifica se não introduziste erros
# (linting, type checking, etc.)
```

Se adicionares features, adiciona testes:

```python
# tests/test_infer.py (exemplo)
import pytest
from src.infer import map_class_name

def test_map_class_name():
    assert map_class_name("RBC") == "RBC"
    assert map_class_name("rbc") == "RBC"
    assert map_class_name("red_blood_cell") == "RBC"
```

### Pull Request

Ao abrir um PR:

1. **Título descritivo**: `feat: add Excel export functionality`
2. **Descrição completa**:
   - O que mudou
   - Porquê
   - Como testar
   - Screenshots (se UI)
   - Issues relacionadas (`Closes #123`)
3. **Checklist**:

```markdown
- [ ] Testei localmente
- [ ] Código segue convenções do projeto
- [ ] Docstrings adicionadas/atualizadas
- [ ] README atualizado (se necessário)
- [ ] Sem erros de linting
- [ ] Commit messages seguem convenção
```

## 📁 Estrutura do Projeto

```
blood_cell_detector/
├── app.py                 # App principal - UI/UX
├── src/
│   ├── infer.py          # Lógica YOLO - adiciona funções aqui
│   └── io_utils.py       # I/O helpers - adiciona utils aqui
├── models/               # Modelos - NÃO commitar .pt
├── tests/                # Testes - adiciona aqui
├── docs/                 # Documentação extra
└── ...
```

### Onde Adicionar Código

- **Nova feature de inferência** → `src/infer.py`
- **Novo tipo de export** → `src/io_utils.py`
- **Nova página/aba UI** → `app.py`
- **Novo utilitário** → criar `src/utils.py` ou similar
- **Testes** → `tests/test_*.py`

## 🐛 Debugging

### Logs

```python
import streamlit as st

# Debug no UI
st.write(f"Debug: {variable}")

# Debug no terminal
print(f"[DEBUG] Value: {value}")
```

### Erros Comuns

| Erro | Solução |
|------|---------|
| Import error | Verifica PYTHONPATH ou estrutura de pastas |
| Model not found | Verifica MODEL_PATH |
| Memory error | Reduz batch size ou usa modelo menor |
| OpenCV error | Instala `libgl1-mesa-glx` |

## 📝 Documentação

Ao adicionar features, atualiza:

- **README.md** - Se afeta uso básico
- **DEPLOYMENT.md** - Se afeta deployment
- **CHANGELOG.md** - Sempre
- Docstrings - Sempre
- Comments inline - Quando lógica complexa

## ❓ Dúvidas?

- Abre uma [Discussion](https://github.com/USER/REPO/discussions)
- Pergunta na Issue relacionada
- Contacta os maintainers

## 🙏 Reconhecimento

Contribuidores serão adicionados ao README e releases notes!

---

**Obrigado por contribuíres!** 🎉

Todos os contribuidores seguem o nosso [Código de Conduta](CODE_OF_CONDUCT.md).
