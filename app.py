"""
Blood Cell Detection App
Aplicação Streamlit para deteção de células sanguíneas usando YOLO.
"""

import streamlit as st
from pathlib import Path
import pandas as pd
from typing import List, Dict, Any
import tempfile
import os
import requests

from src.infer import load_model, run_inference, calculate_metrics
from src.io_utils import (
    load_image,
    create_results_zip,
    create_results_csv,
    validate_image_file
)


# Configuração da página
st.set_page_config(
    page_title="Blood Cell Detector",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração do modelo
# IMPORTANTE: Substitui pelo teu link do Hugging Face
HUGGING_FACE_MODEL_URL = os.getenv(
    "HUGGING_FACE_MODEL_URL",
    "https://huggingface.co/mecaleca/blood-cell-detector-yolo8/resolve/main/best.pt"
)
MODEL_PATH = "models/best.pt"


@st.cache_resource
def download_model_from_huggingface(url: str, save_path: str) -> str:
    """
    Faz download do modelo do Hugging Face se não existir localmente.
    
    Args:
        url: URL do modelo no Hugging Face
        save_path: Caminho onde guardar o modelo
        
    Returns:
        Caminho do modelo
    """
    model_path = Path(save_path)
    
    # Se já existe, retorna
    if model_path.exists():
        return str(model_path)
    
    # Criar diretório se não existir
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download com progress bar
    try:
        with st.spinner("🔽 A fazer download do modelo do Hugging Face... (pode demorar 1-2 min)"):
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(model_path, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
        
        st.success("✅ Modelo descarregado com sucesso!")
        return str(model_path)
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao fazer download do modelo: {str(e)}")
        st.info(f"Verifica se o URL está correto: {url}")
        st.stop()


@st.cache_resource
def get_model(model_path: str):
    """Carrega o modelo YOLO uma única vez (cached)."""
    return load_model(model_path)


def main():
    # Header
    st.title("🔬 Blood Cell Detection System")
    st.markdown("**Deteção automática de células sanguíneas (RBC, WBC, Platelets) usando YOLO**")
    st.divider()
    
    # Download do modelo se necessário
    model_path = download_model_from_huggingface(HUGGING_FACE_MODEL_URL, MODEL_PATH)
    
    # Carregar modelo
    with st.spinner("A carregar modelo YOLO..."):
        try:
            model = get_model(model_path)
            st.success("✅ Modelo carregado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao carregar modelo: {str(e)}")
            st.stop()
    
    # Sidebar - Configurações
    st.sidebar.header("⚙️ Configurações")
    
    confidence_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Limiar mínimo de confiança para deteções"
    )
    
    iou_threshold = st.sidebar.slider(
        "IOU Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.45,
        step=0.05,
        help="Limiar para Non-Maximum Suppression"
    )
    
    show_labels = st.sidebar.checkbox("Mostrar labels", value=True)
    show_conf = st.sidebar.checkbox("Mostrar confidence", value=True)
    
    st.sidebar.divider()
    st.sidebar.info(
        "**Modelo:** YOLO Ultralytics\n\n"
        f"**Classes:** RBC, WBC, Platelets\n\n"
        f"**Source:** Hugging Face"
    )
    
    # Upload de imagens
    st.header("📤 Upload de Imagens")
    uploaded_files = st.file_uploader(
        "Escolhe uma ou mais imagens para análise",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Formatos suportados: JPG, JPEG, PNG"
    )
    
    if not uploaded_files:
        st.info("👆 Faz upload de imagens para começar a análise.")
        return
    
    # Validar ficheiros
    valid_files = []
    for file in uploaded_files:
        if validate_image_file(file):
            valid_files.append(file)
        else:
            st.warning(f"⚠️ Ficheiro ignorado (formato inválido): {file.name}")
    
    if not valid_files:
        st.error("Nenhum ficheiro válido foi carregado.")
        return
    
    st.success(f"✅ {len(valid_files)} imagens válidas carregadas.")
    
    # Botão de deteção
    if st.button("🔍 Run Detection", type="primary", use_container_width=True):
        
        # Containers para resultados
        results_container = st.container()
        metrics_container = st.container()
        
        # Processar imagens
        all_results = []
        annotated_images = {}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, file in enumerate(valid_files):
            status_text.text(f"A processar: {file.name} ({idx + 1}/{len(valid_files)})")
            
            # Carregar imagem
            original_image = load_image(file)
            
            # Inferência
            result = run_inference(
                model=model,
                image=original_image,
                conf_threshold=confidence_threshold,
                iou_threshold=iou_threshold,
                show_labels=show_labels,
                show_conf=show_conf
            )
            
            # Guardar resultados
            result["filename"] = file.name
            all_results.append(result)
            annotated_images[file.name] = result["annotated_image"]
            
            # Atualizar progresso
            progress_bar.progress((idx + 1) / len(valid_files))
        
        status_text.empty()
        progress_bar.empty()
        
        # Calcular métricas agregadas
        total_metrics = calculate_metrics(all_results)
        
        # Mostrar resultados por imagem
        with results_container:
            st.header("📊 Resultados da Deteção")
            
            for result in all_results:
                with st.expander(f"🖼️ {result['filename']}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Original")
                        st.image(result["original_image"], use_container_width=True)
                    
                    with col2:
                        st.subheader("Anotada")
                        st.image(result["annotated_image"], use_container_width=True)
                    
                    # Métricas individuais
                    st.subheader("Contagens")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    
                    counts = result["counts"]
                    percentages = result["percentages"]
                    total = sum(counts.values())
                    
                    with col_m1:
                        st.metric("🔴 RBC", counts.get("RBC", 0), 
                                 f"{percentages.get('RBC', 0):.1f}%")
                    
                    with col_m2:
                        st.metric("⚪ WBC", counts.get("WBC", 0),
                                 f"{percentages.get('WBC', 0):.1f}%")
                    
                    with col_m3:
                        st.metric("🔵 Platelets", counts.get("Platelets", 0),
                                 f"{percentages.get('Platelets', 0):.1f}%")
                    
                    st.caption(f"**Total de células detetadas:** {total}")
        
        # Métricas agregadas
        with metrics_container:
            st.header("📈 Resumo do Batch")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📁 Imagens Processadas", len(all_results))
            
            with col2:
                st.metric("🔴 Total RBC", total_metrics["total_counts"]["RBC"])
            
            with col3:
                st.metric("⚪ Total WBC", total_metrics["total_counts"]["WBC"])
            
            with col4:
                st.metric("🔵 Total Platelets", total_metrics["total_counts"]["Platelets"])
            
            st.subheader("Percentagens Agregadas")
            col_p1, col_p2, col_p3 = st.columns(3)
            
            with col_p1:
                st.metric("RBC %", f"{total_metrics['percentages']['RBC']:.2f}%")
            
            with col_p2:
                st.metric("WBC %", f"{total_metrics['percentages']['WBC']:.2f}%")
            
            with col_p3:
                st.metric("Platelets %", f"{total_metrics['percentages']['Platelets']:.2f}%")
            
            # Tabela detalhada
            st.subheader("📋 Tabela Detalhada")
            df_data = []
            for result in all_results:
                row = {
                    "Filename": result["filename"],
                    "RBC": result["counts"].get("RBC", 0),
                    "WBC": result["counts"].get("WBC", 0),
                    "Platelets": result["counts"].get("Platelets", 0),
                    "Total": sum(result["counts"].values()),
                    "RBC %": f"{result['percentages'].get('RBC', 0):.1f}%",
                    "WBC %": f"{result['percentages'].get('WBC', 0):.1f}%",
                    "Platelets %": f"{result['percentages'].get('Platelets', 0):.1f}%",
                }
                df_data.append(row)
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Botões de download
            st.subheader("💾 Downloads")
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                csv_data = create_results_csv(df)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name="blood_cell_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_d2:
                zip_data = create_results_zip(annotated_images)
                st.download_button(
                    label="🗜️ Download ZIP (Imagens Anotadas)",
                    data=zip_data,
                    file_name="annotated_images.zip",
                    mime="application/zip",
                    use_container_width=True
                )
        
        # Feature Extra: Análise Extra (>50 imagens)
        if len(valid_files) > 50:
            st.divider()
            st.header("🔬 Análise Extra Desbloqueada")
            st.info("**Processaste mais de 50 imagens!** Análise comparativa disponível abaixo.")
            
            with st.expander("⚠️ **AVISO IMPORTANTE - LER ANTES DE CONTINUAR**", expanded=True):
                st.warning(
                    """
                    **IMPORTANTE: Esta não é uma ferramenta de diagnóstico médico**
                    
                    - ❌ Isto **NÃO** é um exame clínico nem diagnóstico
                    - ❌ As contagens em imagens **NÃO** equivalem a valores laboratoriais (ex: hemograma)
                    - ✅ É apenas uma **demonstração educacional** com valores de referência configuráveis
                    - ✅ Os "valores de referência" são placeholders genéricos
                    
                    **Se tens preocupações sobre a tua saúde, consulta um profissional de saúde qualificado.**
                    
                    Esta funcionalidade serve apenas para fins educacionais e de demonstração técnica.
                    """
                )
            
            st.subheader("📝 Informação do Utilizador (Demonstração)")
            
            col_u1, col_u2, col_u3 = st.columns(3)
            
            with col_u1:
                user_age = st.number_input(
                    "Idade *",
                    min_value=1,
                    max_value=120,
                    value=30,
                    help="Obrigatório"
                )
            
            with col_u2:
                user_sex = st.selectbox(
                    "Sexo *",
                    options=["Masculino", "Feminino", "Outro"],
                    help="Obrigatório"
                )
            
            with col_u3:
                user_weight = st.number_input(
                    "Peso (kg)",
                    min_value=0.0,
                    max_value=300.0,
                    value=70.0,
                    help="Opcional"
                )
            
            if st.button("📊 Gerar Comparação (Não Clínica)", type="secondary"):
                st.subheader("Comparação com Valores de Referência (Configuráveis)")
                
                # Valores de referência PLACEHOLDER (editáveis no código)
                reference_ranges = {
                    "RBC": {"min": 40.0, "max": 55.0, "unit": "%"},
                    "WBC": {"min": 0.5, "max": 2.0, "unit": "%"},
                    "Platelets": {"min": 15.0, "max": 40.0, "unit": "%"},
                }
                
                st.caption("**Nota:** Valores de referência são placeholders genéricos para demonstração.")
                
                comparison_data = []
                for cell_type in ["RBC", "WBC", "Platelets"]:
                    observed = total_metrics['percentages'][cell_type]
                    ref_range = reference_ranges[cell_type]
                    
                    status = "Dentro do intervalo configurado"
                    if observed < ref_range["min"]:
                        status = "Abaixo do intervalo configurado"
                    elif observed > ref_range["max"]:
                        status = "Acima do intervalo configurado"
                    
                    comparison_data.append({
                        "Tipo de Célula": cell_type,
                        "Observado": f"{observed:.2f}%",
                        "Intervalo Configurado": f"{ref_range['min']}-{ref_range['max']}%",
                        "Status (Não Clínico)": status
                    })
                
                df_comparison = pd.DataFrame(comparison_data)
                st.dataframe(df_comparison, use_container_width=True, hide_index=True)
                
                st.info(
                    f"""
                    **Dados do utilizador (demonstração):**
                    - Idade: {user_age} anos
                    - Sexo: {user_sex}
                    - Peso: {user_weight if user_weight > 0 else 'Não fornecido'} kg
                    - Total de células analisadas: {sum(total_metrics['total_counts'].values())}
                    
                    **Lembrete:** Esta informação não tem valor clínico. Consulta um profissional de saúde.
                    """
                )


if __name__ == "__main__":
    main()
