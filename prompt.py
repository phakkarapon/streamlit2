import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ฟังก์ชันโหลดภาพจาก URL
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# URL รูปภาพ
image_urls = [
    "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
    "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_1280.jpg"
]

# โหลดภาพทั้งหมด
images = [load_image_from_url(url) for url in image_urls]

st.title("เลือกภาพแมว | ปรับขนาด | แสดงขนาดแกน X/Y")

# แสดง thumbnail ของทั้ง 3 รูป
cols = st.columns(3)
for i, col in enumerate(cols):
    with col:
        if st.button(f"เลือกภาพที่ {i+1}"):
            st.session_state.selected_image = i
        st.image(images[i], use_column_width=True, caption=f"ภาพที่ {i+1}")

# ตรวจสอบว่าผู้ใช้เลือกภาพใด (ค่าเริ่มต้น: ภาพแรก)
selected_index = st.session_state.get("selected_image", 0)
selected_image = images[selected_index]

st.subheader(f"ภาพที่เลือก (ภาพที่ {selected_index+1})")

# Slider สำหรับปรับขนาดภาพ (0.0 - 1.0)
scale = st.slider("ปรับขนาดภาพ (0 = เล็กสุด, 1 = ใหญ่สุด)", 0.0, 1.0, 1.0, step=0.01)

# คำนวณขนาดภาพใหม่
if scale == 0.0:
    resized_width = 100
else:
    resized_width = int(selected_image.width * scale)
resized_height = int(resized_width * selected_image.height / selected_image.width)
resized_image = selected_image.resize((resized_width, resized_height))

# แสดงภาพที่ resize แล้ว
st.image(resized_image, caption=f"ภาพที่ {selected_index+1} (ขนาด: {scale:.2f})")

# แสดงขนาดแกน X/Y
st.write(f"📏 ขนาดภาพปัจจุบัน:")
st.markdown(f"- แกน **X (กว้าง)**: `{resized_width}px`")
st.markdown(f"- แกน **Y (สูง)**: `{resized_height}px`")
