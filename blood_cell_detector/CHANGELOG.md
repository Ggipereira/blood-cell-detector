# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-01

### Added
- 🎉 Release inicial da aplicação
- ✅ Interface web Streamlit para upload de imagens
- ✅ Deteção de células sanguíneas (RBC, WBC, Platelets) com YOLO
- ✅ Visualização lado-a-lado (original vs anotada)
- ✅ Métricas por imagem e agregadas
- ✅ Download de resultados em CSV
- ✅ Download de imagens anotadas em ZIP
- ✅ Configurações ajustáveis (confidence, IOU, labels, etc.)
- ✅ Análise extra desbloqueável para >50 imagens
- ✅ Comparação com valores de referência (demonstrativa)
- ✅ Disclaimers médicos apropriados
- ✅ Model caching para performance
- ✅ Barra de progresso para batch processing
- ✅ Validação de ficheiros de imagem
- ✅ Script CLI para processamento batch (batch_process.py)
- ✅ Script de teste de setup (test_setup.py)
- ✅ Documentação completa (README, DEPLOYMENT)
- ✅ Configuração VSCode (debug, settings)
- ✅ Suporte para mapeamento de classes configurável

### Technical Details
- Python 3.10+
- Streamlit para UI
- Ultralytics YOLO para deteção
- OpenCV para processamento de imagem
- Pandas para análise de dados
- Support para CPU e GPU (automático)

---

## [Unreleased]

### Planned Features
- [ ] Exportar modelo para ONNX (melhor performance CPU)
- [ ] Suporte para vídeo (frame-by-frame)
- [ ] Histórico de análises (session state)
- [ ] Gráficos interativos (plotly/altair)
- [ ] Comparação entre múltiplos batches
- [ ] API REST (FastAPI opcional)
- [ ] Testes unitários (pytest)
- [ ] CI/CD com GitHub Actions
- [ ] Docker container
- [ ] Internacionalização (EN/PT)

---

## Versionamento

- **MAJOR** version: Mudanças incompatíveis na API
- **MINOR** version: Funcionalidades novas compatíveis com versões anteriores
- **PATCH** version: Bug fixes compatíveis com versões anteriores

## Como Contribuir

Para reportar bugs ou sugerir features:
1. Abre uma [Issue](https://github.com/USER/REPO/issues)
2. Descreve o problema/sugestão claramente
3. Inclui screenshots se relevante
4. Menciona a versão do Python e SO

Para contribuir código:
1. Vê [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork o repo
3. Cria um branch para a feature
4. Submete um Pull Request

---

**Legenda:**
- `Added` - Novas features
- `Changed` - Mudanças em features existentes
- `Deprecated` - Features que serão removidas
- `Removed` - Features removidas
- `Fixed` - Bug fixes
- `Security` - Correções de vulnerabilidades
