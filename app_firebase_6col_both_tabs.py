
import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Ép firebase config từ secrets thành dict thuần
firebase_config = {key: st.secrets["firebase"][key] for key in st.secrets["firebase"]}
cred = credentials.Certificate(firebase_config)

# Khởi tạo app Firebase nếu chưa khởi tạo
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# --- phần còn lại của app (giữ nguyên từ file gốc) ---
import streamlit as st
# Thiết lập Firebase
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
    
    # PHÂN TRANG
    if "page_ds" not in st.session_state:
        st.session_state.page_ds = 0

    filtered_docs = []
    for doc in docs:
        item = doc.to_dict()
        if (
            search_ten in item.get("ten_phu_tung", "").lower()
            and search_hang in item.get("hang_xe", "").lower()
            and search_xe in item.get("ten_xe", "").lower()
        ):
            filtered_docs.append((doc.id, item))

    items_per_page = 10
    total_pages = (len(filtered_docs) - 1) // items_per_page + 1
    start = st.session_state.page_ds * items_per_page
    end = start + items_per_page
    paginated_docs = filtered_docs[start:end]

    for doc_id, item in paginated_docs:
        row = st.columns(6)
        row[0].write(item.get("ten_phu_tung", ""))
        row[1].write(item.get("hang_xe", ""))
        row[2].write(item.get("ten_xe", ""))
        row[3].write(item.get("nam_sx", ""))
        row[4].write(item.get("gia_hang", ""))
        row[5].write(item.get("gia_garage", ""))
        if is_admin:
            if st.button(f"🗑️ Xoá", key=doc_id):
                db.collection("phu_tung_data").document(doc_id).delete()
                st.warning("❌ Đã xoá phụ tùng này.")
                st.experimental_rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Trang trước") and st.session_state.page_ds > 0:
            st.session_state.page_ds -= 1
            st.experimental_rerun()
    with col3:
        if st.button("Trang sau ➡️") and st.session_state.page_ds < total_pages - 1:
            st.session_state.page_ds += 1
            st.experimental_rerun()

    st.caption(f"Trang {st.session_state.page_ds + 1} / {total_pages}")
