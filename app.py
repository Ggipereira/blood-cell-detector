import streamlit as st
from PIL import Image
import time
from ultralytics import YOLO
from huggingface_hub import hf_hub_download
import numpy as np
import tensorflow as tf
from tensorflow import keras

# ==================== MODEL LOADING ====================

@st.cache_resource
def load_yolo_ds1_320():
    weights_path = hf_hub_download(
        repo_id="mecaleca/blood-cell-detector-yolo-ds1-320", 
        filename="best320.pt"
    )
    return YOLO(weights_path)

@st.cache_resource
def load_yolo_ds1_640():
    weights_path = hf_hub_download(
        repo_id="mecaleca/blood-cell-detector-yolo-ds1-640", 
        filename="best640.pt"
    )
    return YOLO(weights_path)

@st.cache_resource
def load_yolo_ds2():
    weights_path = hf_hub_download(
        repo_id="mecaleca/blood-cell-detector-yolo-ds2-automatic-fine-tuning", 
        filename="best.pt"
    )
    return YOLO(weights_path)

# @st.cache_resource
# def load_yolo_ds5():
#     weights_path = hf_hub_download(
#         repo_id="mecaleca/blood-cell-detector-yolo-ds5", 
#         filename="best.pt"
#     )
#     return YOLO(weights_path)

import keras
import keras.backend as K

@keras.saving.register_keras_serializable()
def dice_coef(y_true, y_pred, smooth=1):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

@keras.saving.register_keras_serializable()
def dice_loss(y_true, y_pred):
    return 1 - dice_coef(y_true, y_pred)

@keras.saving.register_keras_serializable()
def combined_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    ce = keras.losses.categorical_crossentropy(y_true, y_pred)
    dice = dice_loss(y_true, y_pred)
    return ce + dice

@st.cache_resource
def load_unet():
    from tensorflow import keras
    model_path = hf_hub_download(
        repo_id="Gabriel-26/U_NET_1.0",
        filename="modelo_sangue_unet_sam.keras"
    )
    return keras.models.load_model(
        model_path,
        custom_objects={
            "combined_loss": combined_loss,
            "dice_loss": dice_loss,
            "dice_coef": dice_coef,
        }
    )

@st.cache_resource
def load_efficientnet():
    from tensorflow import keras
    model_path = hf_hub_download(
        repo_id="Gabriel-26/Especialista_WBC_efficientnet",
        filename="modelo_especialista_wbc.keras"
    )
    return keras.models.load_model(model_path)

@st.cache_resource
def load_custom_cnn():
    from tensorflow import keras
    model_path = hf_hub_download(
        repo_id="Gabriel-26/CNN_from_scratch",
        filename="modelo_do_zero.keras"
    )
    return keras.models.load_model(model_path)

# ==================== DETECTION FUNCTIONS ====================

def run_yolo_detection(image, model, conf=0.25):
    img = np.array(image)
    results = model.predict(source=img, conf=conf, verbose=False)
    return results[0]

def run_unet_detection(image, model):
    """
    Runs U-Net segmentation on the input image.
    Expects model input: (1, 256, 256, 3), normalized to [0, 1]
    Expects model output: (1, 256, 256, N_CLASSES) — one channel per class
    Class order assumed: 0=Background, 1=RBC, 2=WBC, 3=Platelet
    """
    original_size = image.size  # (W, H)

    # Preprocess: resize to 256x256 and normalize
    img_resized = image.resize((256, 256))
    img_array = np.array(img_resized, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # (1, 256, 256, 3)

    # Run inference
    prediction = model.predict(img_array, verbose=0)  # (1, 256, 256, N_CLASSES)

    # Get class with highest probability per pixel
    mask = np.argmax(prediction[0], axis=-1)  # (256, 256), values: 0-3

    # Resize mask back to original image size
    mask_resized = np.array(
        Image.fromarray(mask.astype(np.uint8)).resize(original_size, Image.NEAREST)
    )

    return mask_resized


# Class definitions for U-Net output
UNET_CLASSES = {
    0: "Background",
    1: "RBC",
    2: "WBC",
    3: "Platelet",
}

# Colors for each class (RGB) — high contrast, neon-style
UNET_COLORS = {
    0: (0,   0,   0),    # Background — skip
    1: (0,   255, 80),   # RBC — neon green
    2: (255, 50,  255),  # WBC — neon magenta
    3: (255, 200, 0),    # Platelet — neon yellow/orange
}


def unet_mask_to_overlay(image, mask):
    """
    Creates a colored overlay of the segmentation mask on top of the original image.
    Returns a numpy RGB image.
    """
    img_array = np.array(image.convert("RGB"), dtype=np.uint8)
    overlay = img_array.copy()

    color_mask = np.zeros_like(img_array, dtype=np.uint8)
    for class_id, color in UNET_COLORS.items():
        if class_id == 0:
            continue  # Skip background
        color_mask[mask == class_id] = color

    # Blend original image with color mask
    alpha = 0.7
    blended = (img_array * (1 - alpha) + color_mask * alpha).astype(np.uint8)

    # Only replace pixels that belong to a non-background class
    non_bg = mask != 0
    overlay[non_bg] = blended[non_bg]

    return overlay


def unet_mask_to_counts(mask):
    """
    Counts cells per class using connected components, filtering out small fragments.
    """
    from scipy import ndimage

    # Minimum pixel area to be considered a real cell (filters noise/fragments)
    MIN_CELL_AREA = {
        1: 300,   # RBC — medium cells
        2: 500,   # WBC — larger cells
        3: 50,    # Platelet — small, so lower threshold
    }

    counts = {}
    for class_id, class_name in UNET_CLASSES.items():
        if class_id == 0:
            continue
        binary = (mask == class_id).astype(np.uint8)
        labeled_array, num_features = ndimage.label(binary)
        cell_count = 0
        for region_id in range(1, num_features + 1):
            area = np.sum(labeled_array == region_id)
            if area >= MIN_CELL_AREA[class_id]:
                cell_count += 1
        counts[class_name] = cell_count

    return counts


def extract_wbc_crops(image, detections):
    """
    Extracts WBC crops from either YOLO results or U-Net mask.
    - YOLO: crops bounding boxes where class name contains 'wbc' or 'white'
    - U-Net: crops connected components of class 2 (WBC), filtering small fragments
    """
    from scipy import ndimage

    wbc_crops = []
    img_array = np.array(image.convert("RGB"))

    # YOLO path
    if hasattr(detections, "boxes"):
        names = detections.names
        for box, cls_id in zip(detections.boxes.xyxy.cpu().numpy(),
                               detections.boxes.cls.cpu().numpy().astype(int)):
            name_lower = names[cls_id].lower().strip()
            if "wbc" in name_lower or "white" in name_lower:
                x1, y1, x2, y2 = map(int, box)
                # Add small padding around the box
                pad = 5
                x1 = max(0, x1 - pad)
                y1 = max(0, y1 - pad)
                x2 = min(img_array.shape[1], x2 + pad)
                y2 = min(img_array.shape[0], y2 + pad)
                crop = img_array[y1:y2, x1:x2]
                if crop.size > 0:
                    wbc_crops.append(Image.fromarray(crop))

    # U-Net path (class 2 = WBC)
    elif isinstance(detections, np.ndarray):
        wbc_binary = (detections == 2).astype(np.uint8)
        labeled_array, num_features = ndimage.label(wbc_binary)
        for region_id in range(1, num_features + 1):
            region = labeled_array == region_id
            area = np.sum(region)
            if area < 500:  # Skip small fragments
                continue
            rows = np.any(region, axis=1)
            cols = np.any(region, axis=0)
            y1, y2 = np.where(rows)[0][[0, -1]]
            x1, x2 = np.where(cols)[0][[0, -1]]
            # Add padding
            pad = 10
            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(img_array.shape[1], x2 + pad)
            y2 = min(img_array.shape[0], y2 + pad)
            crop = img_array[y1:y2+1, x1:x2+1]
            if crop.size > 0:
                wbc_crops.append(Image.fromarray(crop))

    return wbc_crops

import cv2
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess

# WBC class names (alphabetical order — matches flow_from_directory)
WBC_CLASSES = ["Basophil", "Eosinophil", "Lymphocyte", "Monocyte", "Neutrophil"]

def smart_crop_centered(image_array):
    """
    Replicates the EfficientNet preprocessing: detects the purple nucleus,
    centers and crops around it, resizes to 224x224, then applies EfficientNet preprocess_input.
    """
    if image_array.dtype != np.uint8:
        image_array = np.uint8(image_array)

    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    lower_purple = np.array([100, 40, 40])
    upper_purple = np.array([170, 255, 255])
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        # Fallback: just resize and preprocess
        resized = cv2.resize(image_array, (224, 224), interpolation=cv2.INTER_LINEAR)
        return efficientnet_preprocess(resized.astype(np.float32))

    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cx = x + w // 2
    cy = y + h // 2

    max_side = max(w, h)
    crop_size = int(max_side * 2.5)
    half_size = crop_size // 2

    img_padded = cv2.copyMakeBorder(image_array, crop_size, crop_size, crop_size, crop_size, cv2.BORDER_REFLECT)
    cx_pad = cx + crop_size
    cy_pad = cy + crop_size

    x1 = cx_pad - half_size
    y1 = cy_pad - half_size
    x2 = x1 + crop_size
    y2 = y1 + crop_size

    cropped = img_padded[y1:y2, x1:x2]
    cropped = cv2.resize(cropped, (224, 224), interpolation=cv2.INTER_LINEAR)
    return efficientnet_preprocess(cropped.astype(np.float32))


def preprocess_for_cnn(pil_image):
    """
    Preprocessing for Custom CNN: resize to 128x128, normalize to [0,1].
    """
    img = pil_image.resize((128, 128))
    arr = np.array(img, dtype=np.float32) / 255.0
    return arr


def classify_wbc(wbc_crops, classifier_model, model_name):
    """
    Classifies WBC crops using the given model.
    Returns a dict: { crop_index: { "class": str, "confidence": float, "all_probs": dict } }
    """
    if not wbc_crops:
        return {}

    results = {}
    for i, crop in enumerate(wbc_crops):
        crop_array = np.array(crop.convert("RGB"))

        if model_name == "EfficientNet":
            processed = smart_crop_centered(crop_array)  # (224, 224, 3)
        else:  # Custom CNN
            processed = preprocess_for_cnn(crop)         # (128, 128, 3)

        batch = np.expand_dims(processed, axis=0)
        preds = classifier_model.predict(batch, verbose=0)[0]  # (5,)

        top_idx = int(np.argmax(preds))
        results[i] = {
            "class": WBC_CLASSES[top_idx],
            "confidence": float(preds[top_idx]),
            "all_probs": {WBC_CLASSES[j]: float(preds[j]) for j in range(len(WBC_CLASSES))}
        }

    return results

def load_detection_model(model_name):
    if model_name == "YOLO DS1 (320)":
        return load_yolo_ds1_320()
    elif model_name == "YOLO DS1 (640)":
        return load_yolo_ds1_640()
    elif model_name == "YOLO DS2":
        return load_yolo_ds2()
    elif model_name == "U-Net":
        return load_unet()
    return None

# ==================== EXAMPLE IMAGES ====================

def load_example_images():
    examples = {
        "Blood Sample 1": "examples/BA_393233.jpg",
        "Blood Sample 2": "examples/BA_403405.jpg",
        "Blood Sample 3": "examples/BA_418760.jpg",
        "Blood Sample 4": "examples/BloodImage_00000.jpg",
        "Blood Sample 5": "examples/BloodImage_00001.jpg",
        "Blood Sample 6": "examples/BloodImage_00002.jpg",
        "Blood Sample 7": "examples/test_01.png",
        "Blood Sample 8": "examples/test_02.png",
        "Blood Sample 9": "examples/test_03.png",
        "Blood Sample 10": "examples/test_04.png",
    }
    return examples

# ==================== UI SETUP ====================

st.set_page_config(page_title="BCD - Blood Cell Detector", page_icon="🔬", layout="centered")

st.title("🔬 BCD - Blood Cell Detector")
st.write("Upload a blood cell image and watch our models identify the cells!")

# ==================== SIDEBAR ====================

with st.sidebar:
    st.title("📚 Navigation")
    st.markdown("---")
    st.subheader("🎯 Detection Models")
    st.caption("Choose your detection models")
    st.markdown("---")
    st.subheader("🧬 Classification Models")
    st.caption("Select WBC classifiers")
    st.markdown("---")
    st.info("💡 Compare different models to see the evolution!")

# ==================== MODEL SELECTION ====================

st.subheader("🎯 Detection Model")
det_selection = st.pills(
    "Detection Models",
    ["YOLO DS1 (320)", "YOLO DS1 (640)", "YOLO DS2", "U-Net"],
    selection_mode="multi",
    help="Select one or more detection models to compare side by side"
)

if det_selection and any("YOLO" in m for m in det_selection):
    yolo_conf = st.slider(
        "🎚️ YOLO Confidence Threshold",
        min_value=0.10,
        max_value=0.95,
        value=0.25,
        step=0.05,
        help="Increase to reduce false positives (fewer but more confident detections)"
    )
else:
    yolo_conf = 0.25

st.subheader("🧬 WBC Classification Model")
class_selection = st.pills(
    "Classification Models",
    ["EfficientNet", "Custom CNN"],
    selection_mode="multi",
    help="Select one or more WBC classification models"
)

# ==================== IMAGE INPUT ====================

st.subheader("📸 Image Input")

tab1, tab2, tab3 = st.tabs(["📤 Upload", "📷 Camera", "🖼️ Examples"])

picture = None

with tab1:
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded:
        picture = Image.open(uploaded).convert("RGB")
        st.image(picture, caption="Uploaded Image", use_container_width=True)

with tab2:
    cam = st.camera_input("Take a picture")
    if cam:
        picture = Image.open(cam).convert("RGB")

with tab3:
    examples = load_example_images()
    st.write("Click on an image to select it:")
    
    # Create a grid of images (4 columns)
    cols = st.columns(4)
    
    for idx, (name, path) in enumerate(examples.items()):
        col = cols[idx % 4]
        with col:
            try:
                img = Image.open(path)
                # Use button with image as label
                if st.button(name, key=f"example_{idx}", use_container_width=True):
                    picture = img.convert("RGB")
                    st.session_state['selected_example'] = picture
                    st.session_state['selected_example_name'] = name
                st.image(img, use_container_width=True)
            except:
                st.error(f"❌ {name} not found")
    
    # Display selected image
    if 'selected_example' in st.session_state:
        st.markdown("---")
        st.subheader(f"Selected: {st.session_state['selected_example_name']}")
        picture = st.session_state['selected_example']
        st.image(picture, use_container_width=True)

# ==================== PROCESSING ====================

if st.button("🔬 Run Detection and Classification", type="primary", use_container_width=True):
    if picture is None:
        st.warning("⚠️ Please upload, capture, or select an example image first!")
    elif not det_selection:
        st.warning("⚠️ Please select at least one detection model!")
    else:
        progress_text = "🔄 Processing your image. Please wait..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(40):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)

        # ==================== LOAD & RUN ALL SELECTED MODELS ====================
        all_results = {}  # { model_name: {"model": ..., "detection": ..., "labeled_image": ...} }

        progress_per_model = 40 // len(det_selection)

        for idx, model_name in enumerate(det_selection):
            my_bar.progress(40 + idx * progress_per_model, text=f"⏳ Loading {model_name}...")
            detection_model = load_detection_model(model_name)

            if detection_model is None:
                st.error(f"❌ {model_name} is not available yet!")
                continue

            my_bar.progress(40 + idx * progress_per_model + progress_per_model // 2, text=f"🔍 Running {model_name}...")

            if "YOLO" in model_name:
                detection_results = run_yolo_detection(picture, detection_model, conf=yolo_conf)
                labeled_bgr = detection_results.plot()
                labeled_image = labeled_bgr[:, :, ::-1]
            elif model_name == "U-Net":
                detection_results = run_unet_detection(picture, detection_model)
                labeled_image = unet_mask_to_overlay(picture, detection_results)

            all_results[model_name] = {
                "detection": detection_results,
                "labeled_image": labeled_image,
            }

        my_bar.progress(80, text="✅ Detection complete!")

        # ==================== DISPLAY RESULTS ====================
        st.subheader("📊 Results")

        # Original image always shown first
        st.image(picture, caption="🖼️ Original Image", use_container_width=True)

        if all_results:
            model_names = list(all_results.keys())
            num_models = len(model_names)

            # Show labeled images side by side
            cols = st.columns(num_models)
            for col, model_name in zip(cols, model_names):
                result = all_results[model_name]
                if result["labeled_image"] is not None:
                    col.image(result["labeled_image"], caption=f"🔬 {model_name}", use_container_width=True)
                    if model_name == "U-Net":
                        col.markdown(
                            "🟢 RBC &nbsp;&nbsp; 🟣 WBC &nbsp;&nbsp; 🟡 Platelet",
                            unsafe_allow_html=True
                        )
                else:
                    col.warning(f"⚠️ No output image for {model_name}")

            # ==================== CELL COUNTS SIDE BY SIDE ====================
            st.markdown("### 🩸 Cell Detection Summary")

            count_cols = st.columns(num_models)
            all_wbc_detections = {}

            for col, model_name in zip(count_cols, model_names):
                detection_results = all_results[model_name]["detection"]
                col.markdown(f"**{model_name}**")

                if detection_results is not None and hasattr(detection_results, 'boxes') and len(detection_results.boxes) > 0:
                    cls_ids = detection_results.boxes.cls.cpu().numpy().astype(int)
                    names = detection_results.names

                    # Normalize counts case-insensitively
                    raw_counts = {}
                    for i in cls_ids:
                        name = names[int(i)]
                        raw_counts[name] = raw_counts.get(name, 0) + 1

                    # Map to standard names regardless of case/spacing
                    counts = {"RBC": 0, "WBC": 0, "Platelet": 0}
                    for name, count in raw_counts.items():
                        name_lower = name.lower().strip()
                        if "rbc" in name_lower or "red" in name_lower:
                            counts["RBC"] += count
                        elif "wbc" in name_lower or "white" in name_lower:
                            counts["WBC"] += count
                        elif "platelet" in name_lower or "plt" in name_lower or "platelets" in name_lower:
                            counts["Platelet"] += count

                    col.metric("🔴 RBC", counts.get("RBC", 0))
                    col.metric("⚪ WBC", counts.get("WBC", 0))
                    col.metric("🔵 Platelet", counts.get("Platelet", 0))

                    if counts.get("WBC", 0) > 0:
                        all_wbc_detections[model_name] = detection_results

                elif detection_results is not None and isinstance(detection_results, np.ndarray):
                    counts = unet_mask_to_counts(detection_results)

                    col.metric("🔴 RBC", counts.get("RBC", 0))
                    col.metric("⚪ WBC", counts.get("WBC", 0))
                    col.metric("🔵 Platelet", counts.get("Platelet", 0))

                    if counts.get("WBC", 0) > 0:
                        all_wbc_detections[model_name] = detection_results

                else:
                    col.info("ℹ️ No cells detected.")

            # ==================== WBC CLASSIFICATION ====================
            if all_wbc_detections and class_selection:
                my_bar.progress(85, text="🧬 Extracting WBC regions...")

                st.markdown("---")
                st.subheader("🧬 WBC Classification Results")

                for classifier_name in class_selection:
                    with st.expander(f"📈 {classifier_name} Results", expanded=True):
                        clf_model = load_efficientnet() if classifier_name == "EfficientNet" else load_custom_cnn()

                        if clf_model is None:
                            st.warning(f"⚠️ {classifier_name} model not available!")
                            continue

                        for det_model_name, detection_results in all_wbc_detections.items():
                            st.markdown(f"**Detections from: {det_model_name}**")
                            wbc_crops = extract_wbc_crops(picture, detection_results)

                            if not wbc_crops:
                                st.info("ℹ️ No WBC crops extracted.")
                                continue

                            my_bar.progress(90, text=f"🔬 Classifying with {classifier_name}...")
                            wbc_results = classify_wbc(wbc_crops, clf_model, classifier_name)

                            # Summary count per WBC type
                            type_counts = {}
                            for res in wbc_results.values():
                                cls = res["class"]
                                type_counts[cls] = type_counts.get(cls, 0) + 1

                            st.markdown("**📊 WBC Type Summary:**")
                            summary_cols = st.columns(len(type_counts)) if type_counts else [st]
                            for col, (wbc_type, count) in zip(summary_cols, type_counts.items()):
                                col.metric(wbc_type, count)

                            # Individual crops with predictions
                            st.markdown("**🔬 Individual WBC Classifications:**")
                            n_cols = min(4, len(wbc_crops))
                            crop_cols = st.columns(n_cols)
                            for idx, (crop, res) in enumerate(zip(wbc_crops, wbc_results.values())):
                                col = crop_cols[idx % n_cols]
                                col.image(crop, use_container_width=True)
                                col.markdown(
                                    f"**{res['class']}**  \n"
                                    f"`{res['confidence']*100:.1f}%`"
                                )

                            st.markdown("---")

        # ==================== COMPLETION ====================
        my_bar.progress(100, text="🎉 Complete!")
        time.sleep(0.5)
        my_bar.empty()

        st.balloons()
        st.success("✅ Analysis complete!", icon="🔥")
        
        # ==================== FEEDBACK ====================
        st.markdown("---")
        st.subheader("⭐ Rate this detection")
        feedback = st.feedback("stars")
        if feedback is not None:
            st.success(f"Thanks for rating {feedback + 1} star{'s' if feedback > 0 else ''}! 🙏")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("💡 **Pro Tip**: Upload clear, well-lit blood smear images for best results")
st.caption("🚀 **Model Evolution**: Compare between YOLO and U-Net to see different approaches!")