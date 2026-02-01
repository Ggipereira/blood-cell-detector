"""
Script CLI para processamento batch de imagens (alternativa à app web).
Execute: python batch_process.py --input <pasta> --output <pasta>
"""

import argparse
from pathlib import Path
import sys
from typing import List
import pandas as pd

from src.infer import load_model, run_inference, calculate_metrics
from src.io_utils import load_image, save_image_local


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Blood Cell Detection - Batch Processing"
    )
    
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Pasta com imagens de input"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=True,
        help="Pasta para guardar resultados"
    )
    
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="models/best.pt",
        help="Caminho para o modelo YOLO (default: models/best.pt)"
    )
    
    parser.add_argument(
        "--conf",
        "-c",
        type=float,
        default=0.25,
        help="Confidence threshold (default: 0.25)"
    )
    
    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
        help="IOU threshold (default: 0.45)"
    )
    
    parser.add_argument(
        "--save-annotated",
        action="store_true",
        help="Guardar imagens anotadas"
    )
    
    parser.add_argument(
        "--save-csv",
        action="store_true",
        help="Guardar resultados em CSV"
    )
    
    return parser.parse_args()


def get_image_files(input_dir: Path) -> List[Path]:
    """Obtém lista de ficheiros de imagem numa pasta."""
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    image_files = []
    for ext in valid_extensions:
        image_files.extend(input_dir.glob(f'*{ext}'))
        image_files.extend(input_dir.glob(f'*{ext.upper()}'))
    
    return sorted(image_files)


def main():
    args = parse_args()
    
    # Validar inputs
    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"❌ Erro: Pasta de input não existe: {input_dir}")
        sys.exit(1)
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"❌ Erro: Modelo não encontrado: {model_path}")
        sys.exit(1)
    
    # Obter ficheiros
    image_files = get_image_files(input_dir)
    if not image_files:
        print(f"❌ Erro: Nenhuma imagem encontrada em: {input_dir}")
        sys.exit(1)
    
    print(f"📁 Encontradas {len(image_files)} imagens em: {input_dir}")
    
    # Carregar modelo
    print(f"🤖 A carregar modelo: {model_path}")
    try:
        model = load_model(str(model_path))
        print("✅ Modelo carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        sys.exit(1)
    
    # Processar imagens
    print(f"\n🔍 A processar {len(image_files)} imagens...")
    print(f"   Confidence: {args.conf}")
    print(f"   IOU: {args.iou}")
    print()
    
    all_results = []
    
    for idx, img_path in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] {img_path.name}...", end=" ")
        
        try:
            # Carregar imagem
            with open(img_path, 'rb') as f:
                image = load_image(f)
            
            # Inferência
            result = run_inference(
                model=model,
                image=image,
                conf_threshold=args.conf,
                iou_threshold=args.iou,
                show_labels=True,
                show_conf=True
            )
            
            result["filename"] = img_path.name
            all_results.append(result)
            
            # Guardar imagem anotada se solicitado
            if args.save_annotated:
                output_path = output_dir / f"{img_path.stem}_annotated.png"
                save_image_local(result["annotated_image"], str(output_path))
            
            # Mostrar resumo
            counts = result["counts"]
            total = sum(counts.values())
            print(f"✅ Detetadas {total} células (RBC:{counts['RBC']}, WBC:{counts['WBC']}, PLT:{counts['Platelets']})")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue
    
    # Calcular métricas agregadas
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    metrics = calculate_metrics(all_results)
    
    print(f"Total de imagens processadas: {metrics['num_images']}")
    print(f"Total de células detetadas: {sum(metrics['total_counts'].values())}")
    print()
    print("Contagens por classe:")
    for cls, count in metrics['total_counts'].items():
        pct = metrics['percentages'][cls]
        print(f"  {cls:>10}: {count:>6} ({pct:>5.2f}%)")
    
    # Guardar CSV se solicitado
    if args.save_csv:
        csv_path = output_dir / "results.csv"
        
        df_data = []
        for result in all_results:
            row = {
                "filename": result["filename"],
                "RBC": result["counts"]["RBC"],
                "WBC": result["counts"]["WBC"],
                "Platelets": result["counts"]["Platelets"],
                "Total": sum(result["counts"].values()),
                "RBC_pct": result["percentages"]["RBC"],
                "WBC_pct": result["percentages"]["WBC"],
                "Platelets_pct": result["percentages"]["Platelets"],
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df.to_csv(csv_path, index=False)
        
        print(f"\n💾 CSV guardado em: {csv_path}")
    
    if args.save_annotated:
        print(f"🖼️  Imagens anotadas guardadas em: {output_dir}")
    
    print("\n✅ Processamento concluído!")


if __name__ == "__main__":
    main()
