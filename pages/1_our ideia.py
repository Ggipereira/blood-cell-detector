import streamlit as st

st.set_page_config(page_title="BCD — Our Idea", page_icon="💡", layout="centered")
st.sidebar.title("📚 Navegação")
st.title("💡 Our Idea")
st.write(
    "A robust model that detects and counts white blood cells (WBCs), red blood cells (RBCs), and platelets "
    "across different image types and acquisition conditions, and can also distinguish between WBC subtypes."
)

dot = r"""
digraph BCD {
  rankdir=LR;
  node [shape=box, style="rounded,filled", color="#555555", fillcolor="#F3F4F6"];

  "State-of-the-art review\n+ dataset collection" -> "Data preprocessing" -> "Model training";
  "Model training" -> "U-Net\n(segmentation)";
  "Model training" -> "YOLO\n(detection)";
  "Model training" -> "BCD (from scratch)\n(custom detector)";

  "YOLO\n(detection)" -> "Counts\nRBC / WBC / Platelets" -> "Summary";
  "YOLO\n(detection)" -> "Image with\nbounding boxes";
}
"""

st.subheader("Pipeline")
st.graphviz_chart(dot, use_container_width=True)
