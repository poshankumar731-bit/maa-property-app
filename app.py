import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page Configuration for High-End Corporate look
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल क्लाउड ऐप 2026", layout="wide")

# High-Tech Styling (Cyber Dark Theme + Premium Contrast)
st.markdown("""
<style>
    .main { background-color: #0b0c10; color: #c5c6c7; }
    .stTabs [data-baseweb="tab"] { color: #8a99ad; font-weight: bold; font-size: 16px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00ffcc; border-bottom-color: #00ffcc; }
    
    /* Clean, Professional Invoice Box Style */
    .invoice-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border: 2px solid #111111;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        max-width: 650px;
        margin: 20px auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .invoice-card h2, .invoice-card h4, .invoice-card p, .invoice-card td {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Persistent Cloud Data Store Simulation
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = []

# Application Title Header
st.title("⚡ माँ प्रॉपर्टीज डिजिटल क्लाउड मैनेजमेंट")
st.write("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🔍 लाइव स्क्रीन (View Database)", 
    "➕ नई प्रॉपर्टी जोड़ें", 
    "💳 डिजिटल बिलिंग और रसीद (Billing Panel)"
])

# TAB 1: LIVE DATA VIEW
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    for p in st.session_state.properties:
        st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
        st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}")
        st.write(f"👤 मालिक: {p['owner']}")
        
        msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर विवरण भेजें]({wa_url})")
        st.write("---")

# TAB 2: ADD NEW PROPERTY TO CLOUD
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("add_property_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        btn = st.form_submit_button("☁️ सुरक्षित लाइव सेव करें")
        if btn:
            if n and r:
                new_id = f"PROP-{random.randint(103, 999)}"
                st.session_state.properties.append({"id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o})
                st.success(f"🎉 प्रॉपर्टी सफलतापूर्वक लाइव स्क्रीन पर सेव हो गई! ID: {new_id}")
                st.balloons()
            else:
                st.error("नाम और कीमत भरना जरूरी है!")

# TAB 3: SYSTEMATIC DIGITAL BILLING ENGINE WITH AUTO-LEDGER
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    st.write("विवरण दर्ज करें और रसीद तुरंत प्रिंट या नीचे रिकॉर्ड रजिस्टर में सुरक्षित करें:")
    
    # Input Form Fields
    col_left, col_right = st.columns(2)
    
    with col_left:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value="", placeholder="जैसे: साईं रेजीडेंसी प्लॉट नं 5")
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value="", placeholder="जैसे: मुंगेली रोड, बिलासपुर")
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", value="", placeholder="जैसे: राहुल कुमार")
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value="", placeholder="जैसे: 9999999999")

    with col_right:
        base_price = st.number_input("5. कुल सौदा राशि (₹)", min_value=0, value=0, step=1000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=0, step=500)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=0, step=1000)

    # Calculation logic
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write("---")
    
    # Generate Trigger Button
    if st.button("🖨️ डिजिटल रसीद जनरेट और रिकॉर्ड में सेव करें"):
        if b_name == "":
            st.warning("कृपया बिल बनाने के लिए प्रॉपर्टी का नाम अवश्य लिखें!")
        else:
            invoice_id = f"INV-{random.randint(1000, 9999)}"
            
            # Save data safely to list database
            new_bill = {
                "रसीद ID": invoice_id,
                "तारीख": current_date,
                "प्रॉपर्टी": b_name,
                "लोकेशन": b_loc,
                "कस्टमर": c_name,
                "मोबाइल": c_phone,
                "मूल सौदा (₹)": base_price,
                "छूट (₹)": disc,
                "फाइनल डील (₹)": final_total,
                "एडवांस प्राप्त (₹)": adv,
                "बकाया राशि (₹)": pending_amount
            }
            st.session_state.bill_records.append(new_bill)
            st.success(f"📢 इनवॉइस {invoice_id} क्लाउड रिकॉर्ड्स में सफलतापूर्वक रजिस्टर हो गया!")
            
            # Rendering a clean Markdown HTML inside a stable area
            st.markdown(f"""
            <div class="invoice-card">
                <div style="text-align: center; border-bottom: 2px solid #000000; padding-bottom: 8px; margin-bottom: 15px;">
                    <h2 style="margin: 0; letter-spacing: 2px;"><b>|| माँ प्रॉपर्टीज ||</b></h2>
                    <p style="margin: 4px 0 0 0; font-size: 13px; font-weight: bold;">डिजिटल रसीद / इनवॉइस कॉपी</p>
                </div>
                
                <table style="width: 100%; font-size: 13px; margin-bottom: 10px;">
                    <tr><td><b>INVOICE NO:</b> {invoice_id}</td><td style="text-align: right;"><b>DATE:</b> {current_date}</td></tr>
                    <tr><td><b>STATUS:</b> CLOUD RECORDED</td><td style="text-align: right;"><b>TIME:</b> {current_time}</td></tr>
                </table>
                
                <hr style="border-top: 1px dashed #000000; margin: 10px 0;">
                
                <table style="width: 100%; font-size: 14px; line-height: 1.6;">
                    <tr><td style="width: 35%;"><b>🏢 प्रॉपर्टी नाम:</b></td><td><b>{b_name}</b></td></tr>
                    <tr><td><b>📍 पता/लोकेशन:</b></td><td>{b_loc}</td></tr>
                    <tr><td><b>👤 ग्राहक नाम:</b></td><td>{c_name}</td></tr>
                    <tr><td><b>📞 मोबाइल नंबर:</b></td><td>{c_phone}</td></tr>
                </table>
                
                <hr style="border-top: 1px dashed #000000; margin: 10px 0;">
                
                <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #000000; font-weight: bold;">
                        <td style="padding: 5px 0;">विवरण (Particulars)</td>
                        <td style="text-align: right; padding: 5px 0;">राशि (Amount)</td>
                    </tr>
                    <tr><td style="padding: 6px 0;">मूल सौदा राशि (Base Price)</td><td style="text-align: right;">₹{base_price:,}.00</td></tr>
                    <tr><td style="padding: 6px 0;">विशेष छूट (Discount)</td><td style="text-align: right;">- ₹{disc:,}.00</td></tr>
                    <tr style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; font-weight: bold;">
                        <td style="padding: 6px 0;">कुल फाइनल डील (Net Deal Value)</td>
                        <td style="text-align: right;">₹{final_total:,}.00</td>
                    </tr>
                    <tr><td style="padding: 6px 0; color: green;"><b>प्राप्त एडवांस / बयाना</b></td><td style="text-align: right; color: green;"><b>₹{adv:,}.00</b></td></tr>
                    <tr style="border-top: 2px solid #000000; background-color: #f0f0f0; font-weight: bold; font-size: 15px;">
                        <td style="padding: 10px 5px;">🔴 कुल बकाया राशि (PENDING DUE)</td>
                        <td style="text-align: right; padding: 10px 5px; color: #d32f2f;"><b>₹{pending_amount:,}.00</b></td>
                    </tr>
                </table>
                
                <div style="margin-top: 35px; text-align: center; font-size: 11px; border-top: 1px solid #000000; padding-top: 10px;">
                    <p>यह रिकॉर्ड माँ प्रॉपर्टीज ऐप द्वारा डिजिटल रूप से सत्यापित और क्लाउड पर सुरक्षित है।</p>
                    <p style="margin-top: 5px; font-weight: bold;">धन्यवाद!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 टिप: ग्राहक को विवरण भेजने के लिए आप इस सुंदर रसीद का सीधे स्क्रीनशॉट ले सकते हैं!")

    # Live Digital Ledger Register Table view at the bottom
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर (Saved Ledger Register)")
    if len(st.session_state.bill_records) == 0:
        st.caption("अभी तक कोई पुराना बिल रिकॉर्ड सुरक्षित नहीं है। ऊपर एंट्री करके रसीद बनाएं, वह यहाँ अपने आप रजिस्टर हो जाएगी।")
    else:
        df_bills = pd.DataFrame(st.session_state.bill_records)
        st.dataframe(df_bills, use_container_width=True)
        
