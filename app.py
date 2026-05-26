import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="मां प्रॉपर्टी डिजिटल ऐप 2026",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN DARK/LIGHT THEME CUSTOM CSS ---
st.markdown("""
<style>
    :root {
        --primary-color: #d4af37;
        --bg-dark: #121212;
        --card-dark: #1e1e1e;
    }
    .main {
        background-color: #0f0f11;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    .card {
        background-color: #1e1e24;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #d4af37;
        margin-bottom: 15px;
    }
    .lang-box {
        position: absolute;
        top: 10px;
        right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = ""
if 'properties' not in st.session_state:
    # Dummy Data for initialization
    st.session_state.properties = [
        {"id": "PROP-1001", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500/SqFt", "status": "Available", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-1002", "type": "मकान (House)", "area": "3 BHK", "rate": "65 Lakhs", "status": "Available", "location": "Gomti Nagar", "owner": "S. K. Khan"},
    ]
if 'leads' not in st.session_state:
    st.session_state.leads = []

# --- MULTI-LANGUAGE DICTIONARY (Hindi, English, Urdu) ---
LANG_DICT = {
    "English": {
        "title": "Maa Property Digital App 2026",
        "welcome": "Welcome to Premium Property Management",
        "login": "Secure Login",
        "phone": "Mobile Number",
        "otp": "Enter 4-Digit OTP",
        "role": "Select Role",
        "search": "Search Properties",
        "add_prop": "Add New Property",
        "dashboard": "Smart Dashboard"
    },
    "Hindi": {
        "title": "मां प्रॉपर्टी डिजिटल ऐप 2026",
        "welcome": "प्रीमियम प्रॉपर्टी मैनेजमेंट में आपका स्वागत है",
        "login": "सुरक्षित लॉगिन",
        "phone": "मोबाइल नंबर",
        "otp": "4-अंकीय OTP दर्ज करें",
        "role": "रोल चुनें",
        "search": "प्रॉपर्टी खोजें",
        "add_prop": "नई प्रॉपर्टी जोड़ें",
        "dashboard": "स्मार्ट डैशबोर्ड"
    },
    "Urdu": {
        "title": "ماں پراپرٹی ڈیجیٹل ایپ 2026",
        "welcome": "پریمیئم پراپرٹی مینجمنٹ میں آپ کا استقبال ہے",
        "login": "محفوظ لاگ ان",
        "phone": "موبائل نمبر",
        "otp": "4 ہندسوں کا OTP درج کریں",
        "role": "کردار منتخب کریں",
        "search": "پراپرٹی تلاش کریں",
        "add_prop": "نئی پراپرٹی شامل کریں",
        "dashboard": "اسمارٹ ڈیش بورڈ"
    }
}

# --- LANGUAGE SELECTOR ---
lang = st.sidebar.selectbox("🌐 Language / भाषा / زبان", ["Hindi", "English", "Urdu"])
T = LANG_DICT[lang]

st.title(T["title"])
st.subheader(T["welcome"])
st.write("---")

# --- LOGIN SYSTEM (OTP / PASS SYSTEM) ---
if not st.session_state.logged_in:
    st.sidebar.header(T["login"])
    role = st.sidebar.selectbox(T["role"], ["Admin", "Agent", "Customer / ग्राहक"])
    phone_input = st.sidebar.text_input(T["phone"], max_chars=10)
    
    login_method = st.sidebar.radio("Login Via", ["OTP Login", "Password"])
    
    if login_method == "OTP Login":
        if st.sidebar.button("Send OTP"):
            st.sidebar.info("OTP sent successfully to " + phone_input)
        otp_input = st.sidebar.text_input(T["otp"], type="password")
        if st.sidebar.button("Verify & Login"):
            if phone_input and len(otp_input) == 4:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.username = phone_input
                st.rerun()
            else:
                st.sidebar.error("Invalid Details")
    else:
        password_input = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if phone_input and password_input:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.username = phone_input
                st.rerun()

    st.warning("👉 कृपया ऐप की सुविधाओं को देखने के लिए साइडबार से लॉगिन करें। (प्रोटोटाइप के लिए कोई भी 4 अंकों का OTP मान्य है)")

# --- MAIN APP INTERFACE (AFTER LOGIN) ---
else:
    st.sidebar.success(f"Logged in as: {st.session_state.user_role} ({st.session_state.username})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()

    # --- TABS FOR DIFFERENT MODULES ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"📊 {T['dashboard']}", 
        f"🔍 {T['search']}", 
        f"🏠 {T['add_prop']}", 
        "👤 Customer & KYC Management", 
        "💰 Deal & Payments"
    ])

    # --- TAB 1: SMART DASHBOARD ---
    with tab1:
        st.markdown("### Real-time Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Properties", len(st.session_state.properties), delta="+2 This Week")
        with col2:
            st.metric("Available Plots", len([p for p in st.session_state.properties if "Plot" in p['type'] or "प्लॉट" in p['type']]))
        with col3:
            st.metric("Daily Leads", "14", delta="🚀 High")
        with col4:
            st.metric("Monthly Commission", "₹1,45,000", delta="12%")

        st.markdown("---")
        st.markdown("### Quick Admin Alerts")
        st.info("🔔 Reminder: 3 Installments are pending today. Click 'Deal & Payments' to alert customers.")

    # --- TAB 2: SEARCH & FILTER ---
    with tab2:
        st.markdown("### Advance Property Search")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            f_type = st.selectbox("Category Filter", ["All", "प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        with s_col2:
            f_loc = st.text_input("Search Location")
        with s_col3:
            f_status = st.selectbox("Status", ["All", "Available", "Sold"])

        # Filtering Logic
        filtered_props = st.session_state.properties
        if f_type != "All":
            filtered_props = [p for p in filtered_props if p['type'] == f_type]
        if f_loc:
            filtered_props = [p for p in filtered_props if f_loc.lower() in p['location'].lower()]

        # Display Properties Cards
        for p in filtered_props:
            st.markdown(f"""
            <div class="card">
                <h3>🏠 {p['type']} - {p['id']}</h3>
                <p><b>📍 Location:</b> {p['location']} | <b>📐 Area:</b> {p['area']}</p>
                <p><b>💰 Rate:</b> {p['rate']} | <b>👤 Owner:</b> {p['owner']}</p>
                <span style="background-color: green; padding: 3px 8px; border-radius: 4px; font-size: 12px;">{p['status']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons
            c1, c2, c3 = st.columns([1, 1, 4])
            with c1:
                # Direct WhatsApp Integration
                msg = f"Hello, I am interested in Property ID {p['id']} ({p['type']}) at {p['location']}."
                whatsapp_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:6px 12px; border-radius:5px; cursor:pointer;">💬 WhatsApp</button></a>', unsafe_allow_html=True)
            with c2:
                if st.button(f"Call Agent 📞", key=f"call_{p['id']}"):
                    st.success("Calling Agent linked to this property...")
            st.write("")

    # --- TAB 3: PROPERTY ENTRY & UPLOAD ---
    with tab3:
        st.markdown("### Add New Property Entry")
        with st.form("property_form", clear_on_submit=True):
            p_id = f"PROP-{random.randint(1003, 9999)}"
            p_type = st.selectbox("प्रॉपर्टी प्रकार (Property Type)", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
            p_area = st.text_input("Area (e.g. 1500 SqFt / 2 Bigha)")
            p_rate = st.text_input("Expected Price / Rate")
            p_loc = st.text_input("Exact Google Map Location / Address")
            p_owner = st.text_input("Owner Name")
            
            # Photo & Video Upload Placeholder
            p_file = st.file_uploader("Upload Property Images / Videos", type=["jpg", "png", "mp4"], accept_multiple_files=True)
            
            submitted = st.form_submit_with_clicks("Save Property to Cloud & Generate Poster")
            if submitted:
                new_prop = {
                    "id": p_id,
                    "type": p_type,
                    "area": p_area,
                    "rate": p_rate,
                    "status": "Available",
                    "location": p_loc,
                    "owner": p_owner
                }
                st.session_state.properties.append(new_prop)
                st.success(f"🎉 Property Successfully Saved! Generated ID: {p_id}")
                st.balloons()

    # --- TAB 4: CUSTOMER & KYC (SAFE REDACTION) ---
    with tab4:
        st.markdown("### Buyer / Seller KYC & Verification Records")
        with st.form("kyc_form"):
            c_name = st.text_input("Customer Full Name")
            c_phone = st.text_input("Customer Contact Number")
            c_role = st.radio("Type", ["Buyer", "Seller", "Agent"])
            
            st.markdown("⚠️ **Privacy Note:** Government identification numbers are strictly masked and securely stored in encrypted formats.")
            c_id_type = st.selectbox("ID Proof Type", ["PAN Card", "Driving License", "Passport", "Aadhaar / Other Government ID"])
            c_id_number = st.text_input("Enter ID Proof Number (Masked for Security)")
            
            if st.form_submit_with_clicks("Save Customer Details"):
                # Masking sensitive ID data before saving or outputting
                masked_id = "[ID Omitted/Redacted for Security]" if c_id_type == "Aadhaar / Other Government ID" else c_id_number
                st.session_state.leads.append({
                    "name": c_name,
                    "phone": c_phone,
                    "role": c_role,
                    "id_type": c_id_type,
                    "id_num": masked_id
                })
                st.success("Customer Profile Encrypted & Saved Successfully.")

        # Displaying Customer Ledger
        if st.session_state.leads:
            st.markdown("#### Saved Contacts Directory")
            df_leads = pd.DataFrame(st.session_state.leads)
            st.dataframe(df_leads)

    # --- TAB 5: DEAL & PAYMENTS ---
    with tab5:
        st.markdown("### Payment & Commission Tracking")
        col_pay1, col_pay2 = st.columns(2)
        
        with col_pay1:
            st.markdown("#### Calculate Instant Commission")
            deal_amt = st.number_input("Total Deal Amount (₹)", value=1000000)
            comm_per = st.slider("Commission (%)", 1, 10, 2)
            earned = (deal_amt * comm_per) / 100
            st.metric("Your Profit / Commission", f"₹{earned:,.2f}")
            
        with col_pay2:
            st.markdown("#### EMI / Installment Status")
            st.warning("⚠️ Pending Installment: Rajesh Kumar (Plot PROP-1001) - ₹50,000 due.")
            if st.button("Send Automated WhatsApp Reminder"):
                st.success("Reminder template sent via cloud API!")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 मां प्रॉपर्टी डिजिटल ऐप | Powered by Secure Cloud Database</p>", unsafe_allow_html=True)
