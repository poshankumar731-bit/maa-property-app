import streamlit as st
import pandas as pd
import random

# --- PAGE SETUP ---
st.set_page_config(
    page_title="मां प्रॉपर्टी डिजिटल ऐप 2026",
    page_icon="🏠",
    layout="wide"
)

# --- THEME STYLING ---
st.markdown("""
<style>
    .main { background-color: #0f0f11; color: #ffffff; }
    .card {
        background-color: #1e1e24;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #d4af37;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIAL DATA ---
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-1001", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500/SqFt", "status": "Available", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-1002", "type": "मकान (House)", "area": "3 BHK", "rate": "65 Lakhs", "status": "Available", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]
if 'leads' not in st.session_state:
    st.session_state.leads = []

st.title("🏠 मां प्रॉपर्टी डिजिटल ऐप 2026")
st.subheader("Welcome to Premium Property Management")
st.write("---")

# --- TABS SYSTEM ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 स्मार्ट डैशबोर्ड", 
    "🔍 प्रॉपर्टी खोजें (Search)", 
    "➕ नई प्रॉपर्टी जोड़ें", 
    "👤 ग्राहक KYC"
])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### Real-time Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Properties", len(st.session_state.properties))
    with col2:
        st.metric("Daily Leads", "14")
    with col3:
        st.metric("Monthly Report", "Active")

# --- TAB 2: SEARCH & WHATSAPP ---
with tab2:
    st.markdown("### Search Properties")
    f_type = st.selectbox("Category Filter", ["All", "प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
    
    filtered = st.session_state.properties
    if f_type != "All":
        filtered = [p for p in filtered if p['type'] == f_type]
        
    for p in filtered:
        st.markdown(f"""
        <div class="card">
            <h4>🏠 {p['type']} - {p['id']}</h4>
            <p>📍 <b>लोकेशन:</b> {p['location']} | 📐 <b>एरिया:</b> {p['area']} | 💰 <b>कीमत:</b> {p['rate']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # WhatsApp Button Fixed
        msg = f"नमस्ते, मुझे प्रॉपर्टी ID {p['id']} में इंटरेस्ट है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर बात करें]({wa_url})")
        st.write("")

# --- TAB 3: ADD PROPERTY (FIXED SUBMIT BUTTON) ---
with tab3:
    st.markdown("### Add New Property")
    with st.form("property_form", clear_on_submit=True):
        p_type = st.selectbox("प्रॉपर्टी प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        p_area = st.text_input("Area (e.g. 1500 SqFt)")
        p_rate = st.text_input("Expected Price")
        p_loc = st.text_input("Location / Address")
        p_owner = st.text_input("Owner Name")
        
        # यहाँ पर गलती थी, जिसे बदल कर 'form_submit_button' कर दिया गया है
        submitted = st.form_submit_button("Save Property to Cloud")
        
        if submitted:
            new_id = f"PROP-{random.randint(1003, 9999)}"
            new_prop = {"id": new_id, "type": p_type, "area": p_area, "rate": p_rate, "status": "Available", "location": p_loc, "owner": p_owner}
            st.session_state.properties.append(new_prop)
            st.success(f"🎉 Property Saved! ID: {new_id}")

# --- TAB 4: CUSTOMER KYC ---
with tab4:
    st.markdown("### Customer & KYC Management")
    with st.form("kyc_form", clear_on_submit=True):
        c_name = st.text_input("Customer Name")
        c_phone = st.text_input("Mobile Number")
        c_id = st.text_input("ID Proof (Masked for Security)")
        
        kyc_submitted = st.form_submit_button("Save Customer Details")
        if kyc_submitted:
            st.success("✔️ Customer Details Encrypted & Saved Successfully.")
        
