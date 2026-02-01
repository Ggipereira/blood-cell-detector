"""
Utilitários para Input/Output.
Funções para carregar imagens, criar ZIPs, CSVs, etc.
"""

import io
import zipfile
from typing import Dict, BinaryIO
import numpy as np
from PIL import Image
import pandas as pd


def validate_image_file(file: BinaryIO) -> bool:
    """
    Valida se o ficheiro é uma imagem válida.
    
    Args:
        file: Ficheiro uploaded
        
    Returns:
        True se válido, False caso contrário
    """
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    # Verificar extensão
    file_name = file.name.lower()
    if not any(file_name.endswith(ext) for ext in valid_extensions):
        return False
    
    # Tentar abrir como imagem
    try:
        Image.open(file)
        file.seek(0)  # Reset file pointer
        return True
    except Exception:
        return False


def load_image(file: BinaryIO) -> np.ndarray:
    """
    Carrega uma imagem de um ficheiro uploaded.
    
    Args:
        file: Ficheiro uploaded do Streamlit
        
    Returns:
        Imagem em formato numpy array (RGB)
    """
    image = Image.open(file)
    
    # Converter para RGB (caso seja RGBA, grayscale, etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Converter para numpy array
    image_array = np.array(image)
    
    return image_array


def image_to_bytes(image: np.ndarray, format: str = 'PNG') -> bytes:
    """
    Converte numpy array para bytes (para download).
    
    Args:
        image: Imagem em formato numpy array
        format: Formato da imagem ('PNG', 'JPEG')
        
    Returns:
        Imagem em bytes
    """
    pil_image = Image.fromarray(image)
    
    buf = io.BytesIO()
    pil_image.save(buf, format=format)
    buf.seek(0)
    
    return buf.getvalue()


def create_results_csv(df: pd.DataFrame) -> bytes:
    """
    Cria um CSV a partir de um DataFrame.
    
    Args:
        df: DataFrame com resultados
        
    Returns:
        CSV em bytes
    """
    return df.to_csv(index=False).encode('utf-8')


def create_results_zip(annotated_images: Dict[str, np.ndarray]) -> bytes:
    """
    Cria um ZIP com as imagens anotadas.
    
    Args:
        annotated_images: Dicionário {filename: image_array}
        
    Returns:
        ZIP em bytes
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, image_array in annotated_images.items():
            # Converter imagem para bytes
            img_bytes = image_to_bytes(image_array, format='PNG')
            
            # Adicionar ao ZIP (remover extensão original e adicionar .png)
            base_name = filename.rsplit('.', 1)[0]
            zip_filename = f"{base_name}_annotated.png"
            
            zip_file.writestr(zip_filename, img_bytes)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def save_image_local(image: np.ndarray, path: str, format: str = 'PNG') -> None:
    """
    Guarda uma imagem localmente (útil para debugging).
    
    Args:
        image: Imagem em formato numpy array
        path: Caminho onde guardar
        format: Formato da imagem
    """
    pil_image = Image.fromarray(image)
    pil_image.save(path, format=format)
