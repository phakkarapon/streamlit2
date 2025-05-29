import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ฟังก์ชันโหลดภาพจาก URL
def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# โหลดภาพ
url = "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg"
image = load_image_from_url(url)

st.title("โปรแกรม Flip รูปภาพจาก URL")

# แสดงภาพต้นฉบับ
st.subheader("ภาพต้นฉบับ")
st.image(image, use_container_width = True)

# ตัวเลือกการ flip
flip_option = st.radio("เลือกการ Flip รูปภาพ:", ("ไม่ Flip", "Flip แนวนอน", "Flip แนวตั้ง"))

# ประมวลผลภาพตามที่เลือก
if flip_option == "Flip แนวนอน":
    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
elif flip_option == "Flip แนวตั้ง":
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
else:
    flipped_image = image

# แสดงผลภาพที่ Flip แล้ว
st.subheader("ภาพที่ผ่านการ Flip")
st.image(flipped_image, use_column_width=True)
