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

st.title("Select picture")

# สร้างคอลัมน์สำหรับรูปภาพขนาดเล็ก
cols = st.columns(3)

# สร้างปุ่มคลิกแต่ละรูป
for i, col in enumerate(cols):
    with col:
        if st.button(f"เลือกภาพที่ {i+1}"):
            st.session_state.selected_image = i
        st.image(images[i], use_container_width =True, caption=f"ภาพที่ {i+1}")

# ตรวจสอบว่าผู้ใช้เลือกภาพใด
selected_index = st.session_state.get("selected_image", 0)
st.subheader(f"ภาพที่เลือก (ภาพที่ {selected_index+1})")
st.image(images[selected_index], caption=f"ภาพที่ {selected_index+1}", use_container_width =True)
