import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Thiết lập Firebase
if not firebase_admin._apps:
    import json
    cred = credentials.Certificate(json.loads(st.secrets["firebase"].to_json()))
    firebase_admin.initialize_app(cred)

db = firestore.client()

ADMIN_PASSWORD = "Duy@041100"
is_admin = False

tab = st.radio("📌 Chọn chức năng", ["📥 Nhập phụ tùng", "📋 Danh sách đã lưu"], horizontal=True)

if tab == "📥 Nhập phụ tùng":
    st.title("📥 Nhập thông tin phụ tùng")

    col1, col2 = st.columns(2)

    with col1:
        ten_phu_tung = st.text_input("Tên phụ tùng")
        ten_xe = st.text_input("Tên xe")
        gia_hang = st.text_input("Giá hàng (VNĐ)")

    with col2:
        hang_xe = st.text_input("Hãng xe")
        nam_sx = st.text_input("Năm sản xuất")
        gia_garage = st.text_input("Giá garage (VNĐ)")

    if st.button("📤 Lưu phụ tùng"):
        if ten_phu_tung and hang_xe and ten_xe:
            data = {
                "ten_phu_tung": ten_phu_tung,
                "hang_xe": hang_xe,
                "ten_xe": ten_xe,
                "nam_sx": nam_sx,
                "gia_hang": gia_hang,
                "gia_garage": gia_garage
            }
            db.collection("phu_tung_data").add(data)
            st.success("✅ Đã lưu thông tin phụ tùng!")
        else:
            st.warning("❗ Vui lòng nhập đầy đủ thông tin!")

    st.markdown("### 📋 Danh sách đã nhập")
    header = st.columns(6)
    for i, label in enumerate(["Tên phụ tùng", "Hãng xe", "Tên xe", "Năm SX", "Giá hàng", "Giá garage"]):
        header[i].markdown(f"**{label}**")

    docs = db.collection("phu_tung_data").order_by("ten_phu_tung").stream()
    for doc in docs:
        item = doc.to_dict()
        cols = st.columns(6)
        cols[0].write(item.get("ten_phu_tung", ""))
        cols[1].write(item.get("hang_xe", ""))
        cols[2].write(item.get("ten_xe", ""))
        cols[3].write(item.get("nam_sx", ""))
        cols[4].write(item.get("gia_hang", ""))
        cols[5].write(item.get("gia_garage", ""))

elif tab == "📋 Danh sách đã lưu":
    st.title("📋 Danh sách phụ tùng đã lưu")

    with st.expander("🔐 Đăng nhập quản trị viên để xoá"):
        password = st.text_input("Nhập mật khẩu", type="password")
        if password == ADMIN_PASSWORD:
            is_admin = True
            st.success("✅ Đăng nhập thành công!")
        elif password:
            st.error("❌ Mật khẩu sai!")

    st.markdown("### 🔍 Tìm kiếm")
    c1, c2, c3 = st.columns(3)
    with c1:
        search_ten = st.text_input("Tên phụ tùng").lower()
    with c2:
        search_hang = st.text_input("Hãng xe").lower()
    with c3:
        search_xe = st.text_input("Tên xe").lower()

    st.markdown("### 📋 Kết quả tìm kiếm")
    header = st.columns(6)
    for i, label in enumerate(["Tên phụ tùng", "Hãng xe", "Tên xe", "Năm SX", "Giá hàng", "Giá garage"]):
        header[i].markdown(f"**{label}**")

    docs = db.collection("phu_tung_data").stream()
    for doc in docs:
        item = doc.to_dict()
        if (
            search_ten in item.get("ten_phu_tung", "").lower()
            and search_hang in item.get("hang_xe", "").lower()
            and search_xe in item.get("ten_xe", "").lower()
        ):
            row = st.columns(6)
            row[0].write(item.get("ten_phu_tung", ""))
            row[1].write(item.get("hang_xe", ""))
            row[2].write(item.get("ten_xe", ""))
            row[3].write(item.get("nam_sx", ""))
            row[4].write(item.get("gia_hang", ""))
            row[5].write(item.get("gia_garage", ""))
            if is_admin:
                if st.button(f"🗑️ Xoá", key=doc.id):
                    db.collection("phu_tung_data").document(doc.id).delete()
                    st.warning("❌ Đã xoá phụ tùng này.")
                    st.experimental_rerun()