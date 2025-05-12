
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Khởi tạo Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate({key: st.secrets["firebase"][key] for key in st.secrets["firebase"]})
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📥 Nhập thông tin phụ tùng")

# Khởi tạo giá trị mặc định cho session_state nếu chưa có
fields = ["ten_phu_tung", "hang_xe", "ten_xe", "nam_sx", "gia_hang", "gia_garage"]
for field in fields:
    if field not in st.session_state:
        st.session_state[field] = ""

# Form thủ công với text_input được điều khiển bởi session_state
st.session_state["ten_phu_tung"] = st.text_input("Tên phụ tùng", value=st.session_state["ten_phu_tung"], key="ten_phu_tung_input")
st.session_state["hang_xe"] = st.text_input("Hãng xe", value=st.session_state["hang_xe"], key="hang_xe_input")
st.session_state["ten_xe"] = st.text_input("Tên xe", value=st.session_state["ten_xe"], key="ten_xe_input")
st.session_state["nam_sx"] = st.text_input("Năm sản xuất", value=st.session_state["nam_sx"], key="nam_sx_input")
st.session_state["gia_hang"] = st.text_input("Giá hàng (VND)", value=st.session_state["gia_hang"], key="gia_hang_input")
st.session_state["gia_garage"] = st.text_input("Giá garage (VND)", value=st.session_state["gia_garage"], key="gia_garage_input")

if st.button("💾 Lưu phụ tùng"):
    data = {
        "ten_phu_tung": st.session_state["ten_phu_tung"],
        "hang_xe": st.session_state["hang_xe"],
        "ten_xe": st.session_state["ten_xe"],
        "nam_sx": st.session_state["nam_sx"],
        "gia_hang": st.session_state["gia_hang"],
        "gia_garage": st.session_state["gia_garage"]
    }

    db.collection("phutung").add(data)
    st.success("✅ Đã lưu thông tin phụ tùng!")

    # Reset từng giá trị session
    for field in fields:
        st.session_state[field] = ""
        st.session_state[field + "_input"] = ""

    st.experimental_rerun()

# Hiển thị dữ liệu đã lưu
st.markdown("## 📋 Danh sách đã nhập")
phu_tung_docs = db.collection("phutung").stream()

cols = st.columns(6)
for i, header in ["Tên phụ tùng", "Hãng xe", "Tên xe", "Năm SX", "Giá hàng", "Giá garage"]:
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
