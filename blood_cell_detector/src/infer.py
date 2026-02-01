"""
Módulo de inferência com YOLO.
Funções para carregar modelo, executar deteção e calcular métricas.
"""

from ultralytics import YOLO
import numpy as np
import cv2
from typing import Dict, List, Any, Tuple
from PIL import Image


def load_model(model_path: str) -> YOLO:
    """
    Carrega o modelo YOLO a partir do caminho especificado.
    
    Args:
        model_path: Caminho para o ficheiro .pt do modelo
        
    Returns:
        Modelo YOLO carregado
        
    Raises:
        FileNotFoundError: Se o ficheiro do modelo não existir
        Exception: Se houver erro ao carregar o modelo
    """
    try:
        model = YOLO(model_path)
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
    except Exception as e:
        raise Exception(f"Erro ao carregar modelo: {str(e)}")


def run_inference(
    model: YOLO,
    image: np.ndarray,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
    show_labels: bool = True,
    show_conf: bool = True
) -> Dict[str, Any]:
    """
    Executa inferência numa imagem e retorna resultados.
    
    Args:
        model: Modelo YOLO carregado
        image: Imagem em formato numpy array (RGB)
        conf_threshold: Limiar de confiança
        iou_threshold: Limiar de IOU para NMS
        show_labels: Se True, mostra labels nas deteções
        show_conf: Se True, mostra confiança nas deteções
        
    Returns:
        Dicionário com:
            - original_image: imagem original
            - annotated_image: imagem com bounding boxes
            - counts: contagens por classe
            - percentages: percentagens por classe
            - detections: lista de deteções raw
    """
    # Executar predição
    results = model.predict(
        image,
        conf=conf_threshold,
        iou=iou_threshold,
        verbose=False
    )[0]
    
    # Obter imagem anotada
    annotated_image = results.plot(
        labels=show_labels,
        conf=show_conf,
        line_width=2,
        font_size=12
    )
    
    # Converter de BGR para RGB (OpenCV usa BGR)
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    
    # Extrair deteções
    detections = []
    counts = {"RBC": 0, "WBC": 0, "Platelets": 0}
    
    if results.boxes is not None and len(results.boxes) > 0:
        for box in results.boxes:
            # Extrair informação da deteção
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            bbox = box.xyxy[0].cpu().numpy()
            
            # Obter nome da classe
            class_name = model.names[class_id]
            
            # Mapear nomes de classes (caso não sejam exatamente RBC/WBC/Platelets)
            class_name_mapped = map_class_name(class_name)
            
            # Atualizar contagens
            if class_name_mapped in counts:
                counts[class_name_mapped] += 1
            
            # Guardar deteção
            detections.append({
                "class": class_name_mapped,
                "confidence": confidence,
                "bbox": bbox.tolist()
            })
    
    # Calcular percentagens
    total = sum(counts.values())
    percentages = {
        cls: (count / total * 100) if total > 0 else 0.0
        for cls, count in counts.items()
    }
    
    return {
        "original_image": image,
        "annotated_image": annotated_image,
        "counts": counts,
        "percentages": percentages,
        "detections": detections
    }


def map_class_name(class_name: str) -> str:
    """
    Mapeia nomes de classes do modelo para nomes standard.
    
    Útil se o modelo usar nomes diferentes (ex: 'red_blood_cell' -> 'RBC').
    Adiciona mapeamentos conforme necessário.
    
    Args:
        class_name: Nome da classe do modelo
        
    Returns:
        Nome da classe mapeado
    """
    # Dicionário de mapeamento (configurável)
    mapping = {
        # Adicionar mapeamentos se necessário, ex:
        # "red_blood_cell": "RBC",
        # "white_blood_cell": "WBC",
        # "platelet": "Platelets",
        
        # Por defeito, nomes standard
        "RBC": "RBC",
        "WBC": "WBC",
        "Platelets": "Platelets",
        
        # Variações comuns
        "rbc": "RBC",
        "wbc": "WBC",
        "platelets": "Platelets",
        "platelet": "Platelets",
    }
    
    return mapping.get(class_name, class_name)


def calculate_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula métricas agregadas a partir de múltiplos resultados.
    
    Args:
        results: Lista de resultados de inferência
        
    Returns:
        Dicionário com métricas agregadas:
            - total_counts: contagens totais por classe
            - percentages: percentagens agregadas
            - num_images: número de imagens processadas
    """
    total_counts = {"RBC": 0, "WBC": 0, "Platelets": 0}
    
    for result in results:
        for cls, count in result["counts"].items():
            if cls in total_counts:
                total_counts[cls] += count
    
    # Calcular percentagens
    total = sum(total_counts.values())
    percentages = {
        cls: (count / total * 100) if total > 0 else 0.0
        for cls, count in total_counts.items()
    }
    
    return {
        "total_counts": total_counts,
        "percentages": percentages,
        "num_images": len(results)
    }


def get_model_info(model: YOLO) -> Dict[str, Any]:
    """
    Retorna informação sobre o modelo.
    
    Args:
        model: Modelo YOLO carregado
        
    Returns:
        Dicionário com informação do modelo
    """
    return {
        "model_type": model.type,
        "class_names": model.names,
        "num_classes": len(model.names) if model.names else 0
    }
