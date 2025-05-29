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

st.title("เลือกภาพแมวเพื่อดูขนาดใหญ่ และปรับขนาดภาพ")

# สร้างคอลัมน์สำหรับรูปภาพขนาดเล็ก
cols = st.columns(3)

# สร้างปุ่มคลิกแต่ละรูป
for i, col in enumerate(cols):
    with col:
        if st.button(f"เลือกภาพที่ {i+1}"):
            st.session_state.selected_image = i
        st.image(images[i], use_column_width=True, caption=f"ภาพที่ {i+1}")

# ตรวจสอบว่าผู้ใช้เลือกภาพใด (ค่าเริ่มต้นคือ 0)
selected_index = st.session_state.get("selected_image", 0)
selected_image = images[selected_index]

st.subheader(f"ภาพที่เลือก (ภาพที่ {selected_index+1})")

# เพิ่มแถบเลื่อนสำหรับปรับขนาด (0.0 ถึง 1.0)
scale = st.slider("ปรับขนาดภาพ", 0.0, 1.0, 1.0, step=0.01)

# ขนาดขั้นต่ำ: 100px หรือเล็กกว่า ถ้า scale ต่ำ
min_size = 100

# ปรับขนาดภาพตาม scale
if scale == 0.0:
    resized_image = selected_image.resize((min_size, int(min_size * selected_image.height / selected_image.width)))
else:
    width = int(selected_image.width * scale)
    height = int(selected_image.height * scale)
    resized_image = selected_image.resize((width, height))

# แสดงภาพที่ resize แล้ว
st.image(resized_image, caption=f"ภาพที่ {selected_index+1} (ขนาด: {scale:.2f})")
