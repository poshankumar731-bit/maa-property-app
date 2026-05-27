import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Maa Property 2026", layout="wide")

# प्रिंट के लिए CSS
st.markdown("""
<style>
    .print-area { width: 100%; max-width: 450px; border: 3px solid #000; padding: 25px; margin: auto; font-family: sans-serif; background: white; color: black; }
    @media print {
        body * { visibility: hidden; }
        .printable, .printable * { visibility: visible; }
        .printable { position: absolute; left: 0; top: 0; width: 100%; }
        @page { size: auto; margin: 10mm; }
    }
</style>
""", unsafe_allow_html=True)

# लॉगिन
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    u = st.text_input("यूजर आईडी")
    p = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if u == "admin" and p == "12345": st.session_state.logged_in = True; st.rerun()
    st.stop()

# डेटा स्टोर
if 'bills' not in st.session_state: st.session_state.bills = []

st.title("⚡ मां प्रॉपर्टी 2026")

tab1, tab2 = st.tabs(["➕ नई रसीद / एडिट", "📜 हिस्ट्री / डिलीट"])

with tab1:
    # अगर एडिट करना है तो डेटा भरें
    b_name = st.text_input("प्रॉपर्टी का नाम")
    khasra = st.text_input("खसरा नंबर")
    area = st.text_input("एरिया (SqFt)")
    c_name = st.text_input("खरीदार का नाम")
    c_phone = st.text_input("खरीदार मोबाइल")
    base = st.number_input("कुल राशि", value=0)
    adv = st.number_input("एडवांस", value=0)
    
    if st.button("रसीद सेव करें"):
        new_bill = {
            "id": random.randint(1000, 9999), "b_name": b_name.upper(), "khasra": khasra,
            "area": area, "c_name": c_name.upper(), "c_phone": c_phone, 
            "base": base, "due": base - adv, "date": datetime.now().strftime('%d-%m-%Y')
        }
        st.session_state.bills.append(new_bill)
        st.session_state.active_bill = new_bill
        st.success("रसीद सेव हो गई!")

    if 'active_bill' in st.session_state:
        rb = st.session_state.active_bill
        st.markdown(f"""
        <div class="printable print-area">
            <h2 style="text-align:center;">MAA PROPERTIES MUNGELI</h2>
            <p style="text-align:center;"><b>Contact: 6264024293</b></p>
            <hr>
            <p><b>Inv:</b> {rb['id']} | <b>Date:</b> {rb['date']}</p>
            <p><b>Property:</b> {rb['b_name']} | <b>Khasra:</b> {rb['khasra']}</p>
            <p><b>Area:</b> {rb['area']} SqFt</p>
            <p><b>Buyer:</b> {rb['c_name']} | <b>Ph:</b> {rb['c_phone']}</p>
            <p><b>Total:</b> ₹{rb['base']:,} | <b>Due:</b> ₹{rb['due']:,}</p>
            <br>
            <div style="display:flex; justify-content: space-between;">
                <div>_______<br>Buyer</div><div>_______<br>Seller</div>
            </div>
            <p style="text-align:center;"><b>Proprietor: VISHAL GUPTA</b></p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🖨️ प्रिंट करने के लिए Ctrl + P दबाएं।")

with tab2:
    st.subheader("📜 बिल हिस्ट्री (यहाँ से डिलीट करें)")
    for i, b in enumerate(st.session_state.bills):
        c1, c2 = st.columns([4, 1])
        c1.write(f"🆔 {b['id']} | 👤 {b['c_name']} | खसरा: {b['khasra']}")
        if c2.button("🗑️ डिलीट", key=i):
            st.session_state.bills.pop(i)
            st.rerun()
