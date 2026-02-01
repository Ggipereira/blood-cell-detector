"""
Script de teste rápido para verificar se tudo está configurado corretamente.
Execute: python test_setup.py
"""

import sys
from pathlib import Path


def test_imports():
    """Testa se todas as dependências estão instaladas."""
    print("🔍 A testar imports...")
    
    try:
        import streamlit
        print("✅ Streamlit instalado:", streamlit.__version__)
    except ImportError:
        print("❌ Streamlit NÃO instalado")
        return False
    
    try:
        import ultralytics
        print("✅ Ultralytics instalado:", ultralytics.__version__)
    except ImportError:
        print("❌ Ultralytics NÃO instalado")
        return False
    
    try:
        import cv2
        print("✅ OpenCV instalado:", cv2.__version__)
    except ImportError:
        print("❌ OpenCV NÃO instalado")
        return False
    
    try:
        import PIL
        print("✅ Pillow instalado:", PIL.__version__)
    except ImportError:
        print("❌ Pillow NÃO instalado")
        return False
    
    try:
        import numpy
        print("✅ NumPy instalado:", numpy.__version__)
    except ImportError:
        print("❌ NumPy NÃO instalado")
        return False
    
    try:
        import pandas
        print("✅ Pandas instalado:", pandas.__version__)
    except ImportError:
        print("❌ Pandas NÃO instalado")
        return False
    
    return True


def test_structure():
    """Verifica se a estrutura de pastas está correta."""
    print("\n📁 A verificar estrutura de ficheiros...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/infer.py",
        "src/io_utils.py",
    ]
    
    required_dirs = [
        "src",
        "models",
    ]
    
    all_ok = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} NÃO encontrado")
            all_ok = False
    
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ NÃO encontrado")
            all_ok = False
    
    return all_ok


def test_model():
    """Verifica se o modelo existe."""
    print("\n🤖 A verificar modelo YOLO...")
    
    model_path = Path("models/best.pt")
    
    if model_path.exists():
        print(f"✅ Modelo encontrado: {model_path}")
        print(f"   Tamanho: {model_path.stat().st_size / (1024*1024):.2f} MB")
        return True
    else:
        print(f"⚠️  Modelo NÃO encontrado em: {model_path}")
        print("   Coloca o ficheiro best.pt na pasta models/")
        return False


def test_src_modules():
    """Testa se os módulos src podem ser importados."""
    print("\n📦 A testar módulos src...")
    
    try:
        from src.infer import load_model, run_inference, calculate_metrics
        print("✅ src.infer importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar src.infer: {e}")
        return False
    
    try:
        from src.io_utils import load_image, validate_image_file
        print("✅ src.io_utils importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar src.io_utils: {e}")
        return False
    
    return True


def main():
    print("="*60)
    print("🔬 BLOOD CELL DETECTOR - TESTE DE CONFIGURAÇÃO")
    print("="*60)
    
    results = {
        "Imports": test_imports(),
        "Estrutura": test_structure(),
        "Modelo": test_model(),
        "Módulos src": test_src_modules(),
    }
    
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print("\n")
    
    if all(results.values()):
        print("🎉 Tudo configurado corretamente!")
        print("   Podes executar: streamlit run app.py")
        return 0
    else:
        print("⚠️  Alguns testes falharam. Verifica os erros acima.")
        if not results["Modelo"]:
            print("\n💡 Dica: Não te esqueças de colocar o best.pt na pasta models/")
        if not results["Imports"]:
            print("\n💡 Dica: Executa 'pip install -r requirements.txt'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
