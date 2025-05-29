import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ฟังก์ชันโหลดภาพจาก URL
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGBA")  # รองรับ transparency

# URL ของรูปภาพทั้ง 2
url1 = "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg"
url2 = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg"

# โหลดรูปภาพ
img1 = load_image_from_url(url1)
img2 = load_image_from_url(url2)

# ปรับขนาดให้เท่ากันตามรูปที่เล็กที่สุด
common_size = (
    min(img1.width, img2.width),
    min(img1.height, img2.height)
)
img1_resized = img1.resize(common_size)
img2_resized = img2.resize(common_size)

st.title("🧪 Blending 2 รูปภาพแมว")

# แสดงรูปภาพต้นฉบับ (หลัง resize)
st.subheader("🔍 รูปต้นฉบับที่ใช้ Blending")
col1, col2 = st.columns(2)
col1.image(img1_resized, caption="รูปที่ 1", use_container_width =True)
col2.image(img2_resized, caption="รูปที่ 2", use_container_width =True)

# Slider สำหรับปรับระดับการ Blending
st.subheader("🎛️ ปรับระดับการ Blending")
blend_ratio = st.slider("0 = รูป 1 เด่น | 1 = รูป 2 เด่น", 0.0, 1.0, 0.5, step=0.01)

# ทำการ Blend ภาพ
blended_image = Image.blend(img1_resized, img2_resized, alpha=blend_ratio)

# แสดงผลภาพที่ผสมแล้ว
st.subheader("🖼️ ภาพที่ได้จากการ Blending")
st.image(blended_image, caption=f"Blend Ratio: {blend_ratio:.2f}", use_container_width =True)
