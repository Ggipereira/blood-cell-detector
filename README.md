# Blood Cell Detector (Streamlit)

A **Streamlit** web app for **detecting and counting blood cells** in microscopy images (e.g., RBC, WBC and platelets), with an optional **WBC subtype classifier** (when enabled in the UI).

> ⚠️ **Disclaimer**  
> This is an **academic/demo** project. It is **not** a medical device and must **not** be used for clinical decision-making.

---

## Live demo (Streamlit Cloud)
The app is available at:  
https://blood-cell-detector.streamlit.app

---

## Key features
- Upload peripheral blood microscopy images
- **Bounding-box detection** (YOLO-based pipeline)
- Class-wise counts (RBC / WBC / Platelets)
- Adjustable **confidence threshold** (and other UI parameters, depending on the version)
- (Optional) **WBC subtype classification** on cropped detections
- Multi-page layout via `pages/` (Streamlit multipage)

---

## Repository structure

```
.
├─ app.py                # Streamlit app entry point
├─ pages/                # Additional pages (Streamlit multipage)
├─ examples/             # Example images / demo inputs
├─ images/               # Static assets (e.g., team photos, UI assets)
├─ requirements.txt      # Python dependencies
├─ packages.txt          # System dependencies (for deployment, e.g., OpenCV)
└─ .gitignore
```

---

## Run locally

### 1) Requirements
- Python 3.10+ (recommended)
- `pip` / `venv`

### 2) Create a virtual environment and install dependencies
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Start the app
```bash
streamlit run app.py
```

The app should open in your browser (default: `http://localhost:8501`).

---

## Deploy to Streamlit Community Cloud
1. Push the repository to GitHub.
2. In Streamlit Cloud, select:
   - **Repository**: your repo
   - **Branch**: `main` (or another)
   - **Main file path**: `app.py`

### Note on `packages.txt`
If you use OpenCV (or other libraries requiring system packages), Streamlit Cloud may need `packages.txt`.  
Keep it in the repo root and list the required system dependencies there (e.g., libraries needed by `opencv-python`).

---

## How to use (in the app)
1. Upload a microscopy image.
2. Select the model (if your UI provides a model selector).
3. Adjust the **confidence threshold** as needed:
   - **higher** → fewer detections (fewer false positives)
   - **lower** → more detections (more sensitive, may increase false positives)
4. View detections + class-wise counts.
5. (Optional) enable WBC classification (if available) to get subtypes.

---

## Troubleshooting

### OpenCV errors on deployment
- Make sure `requirements.txt` includes the correct package (e.g., `opencv-python` or `opencv-python-headless`).
- If system libraries are required, add them to `packages.txt`.

### “Module not found”
- Ensure you installed `requirements.txt` in the active environment.
- If you added new dependencies, update `requirements.txt`.

---

## Contributors
- Diogo Casquinha  
- Vicente Soares  
- Guilherme Pereira  
- Gabriel Afonso  

Supervisor: Simão Gonçalves  
Institution: NOVA Executive Education & Samsung

---

## License
Add a license depending on your project requirements (e.g., MIT, Apache-2.0, or “All rights reserved”).  
If you don’t have one yet, create a `LICENSE` file and choose an appropriate license.
