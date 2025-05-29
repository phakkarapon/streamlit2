import streamlit as st
import torch
from PIL import Image
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# โหลดโมเดลตรวจจับวัตถุ
@st.cache_resource
def load_model():
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

# ฟังก์ชันโหลดรูปจาก URL
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

# ฟังก์ชันตรวจจับวัตถุในภาพ
def detect_objects(image, model, threshold=0.5):
    transform = transforms.Compose([transforms.ToTensor()])
    img_tensor = transform(image)
    with torch.no_grad():
        prediction = model([img_tensor])[0]
    
    boxes = prediction['boxes']
    labels = prediction['labels']
    scores = prediction['scores']
    
    # filter ตาม threshold
    keep = scores > threshold
    return boxes[keep], labels[keep], scores[keep]

# โหลดคลาสชื่อของ COCO dataset
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella',
    'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass', 'cup', 'fork',
    'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
    'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A', 'toilet',
    'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# ─────────────── Streamlit UI ───────────────
st.title("🧠 ตรวจจับวัตถุในภาพ")

model = load_model()

# เลือกแหล่งภาพ
option = st.radio("เลือกรูปภาพ:", ["URL", "อัปโหลดจากเครื่อง"])

if option == "URL":
    url = st.text_input("ใส่ URL ของภาพ", "")
    if url:
        image = load_image_from_url(url)
elif option == "อัปโหลดจากเครื่อง":
    uploaded = st.file_uploader("เลือกรูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")

# ถ้ามีภาพให้วิเคราะห์
if 'image' in locals():
    st.image(image, caption="ภาพต้นฉบับ", use_column_width=True)

    threshold = st.slider("Threshold ความมั่นใจ", 0.0, 1.0, 0.5, step=0.05)
    boxes, labels, scores = detect_objects(image, model, threshold)

    # แสดงภาพพร้อมกรอบ
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    for box, label, score in zip(boxes, labels, scores):
        x1, y1, x2, y2 = box
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                 linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        ax.text(x1, y1 - 5, f"{COCO_INSTANCE_CATEGORY_NAMES[label]} ({score:.2f})", color='white',
                bbox=dict(facecolor='red', alpha=0.5))

    st.pyplot(fig)

    # แสดงรายการวัตถุที่พบ
    detected_objects = {COCO_INSTANCE_CATEGORY_NAMES[label]: f"{score:.2f}" for label, score in zip(labels, scores)}
    st.subheader("📋 วัตถุที่พบในภาพ:")
    for obj, conf in detected_objects.items():
        st.write(f"- {obj} (ความมั่นใจ: {conf})")
