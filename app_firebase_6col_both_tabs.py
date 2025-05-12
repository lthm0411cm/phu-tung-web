
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Khởi tạo Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate({key: st.secrets["firebase"][key] for key in st.secrets["firebase"]})
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📥 Nhập thông tin phụ tùng")

# Inputs ngoài st.form
ten_phu_tung = st.text_input("Tên phụ tùng", key="ten_phu_tung")
hang_xe = st.text_input("Hãng xe", key="hang_xe")
ten_xe = st.text_input("Tên xe", key="ten_xe")
nam_sx = st.text_input("Năm sản xuất", key="nam_sx")
gia_hang = st.text_input("Giá hàng (VND)", key="gia_hang")
gia_garage = st.text_input("Giá garage (VND)", key="gia_garage")

if st.button("💾 Lưu phụ tùng"):
    data = {
        "ten_phu_tung": ten_phu_tung,
        "hang_xe": hang_xe,
        "ten_xe": ten_xe,
        "nam_sx": nam_sx,
        "gia_hang": gia_hang,
        "gia_garage": gia_garage
    }
    db.collection("phutung").add(data)
    st.success("✅ Đã lưu thông tin phụ tùng!")

    for key in ["ten_phu_tung", "hang_xe", "ten_xe", "nam_sx", "gia_hang", "gia_garage"]:
        del st.session_state[key]
    st.rerun()

# Hiển thị dữ liệu đã lưu
st.markdown("## 📋 Danh sách đã nhập")
phu_tung_docs = db.collection("phutung").stream()

cols = st.columns(6)
for i, header in enumerate(["Tên phụ tùng", "Hãng xe", "Tên xe", "Năm SX", "Giá hàng", "Giá garage"]):
    cols[i].markdown(f"**{header}**")

for doc in phu_tung_docs:
    item = doc.to_dict()
    cols = st.columns(6)
    cols[0].write(item.get("ten_phu_tung", ""))
    cols[1].write(item.get("hang_xe", ""))
    cols[2].write(item.get("ten_xe", ""))
    cols[3].write(item.get("nam_sx", ""))
    cols[4].write(item.get("gia_hang", ""))
    cols[5].write(item.get("gia_garage", ""))
