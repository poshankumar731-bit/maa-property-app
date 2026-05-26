import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page configuration
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# Custom Styling & Print Setup
st.markdown("""
<style>
    .main { background-color: #0f111a; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { color: #8a99ad; font-weight: bold; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00ffcc; border-bottom-color: #00ffcc; }
    
    /* Clean, Professional Invoice Box Style */
    .invoice-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border: 2px solid #000000;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
        max-width: 600px;
        margin: 20px auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .invoice-card h2, .invoice-card h4, .invoice-card p, .invoice-card td, .invoice-card th {
        color: #000000 !important;
    }
    
    /* Print trigger style to isolate the receipt paper */
    @media print {
        body * { visibility: hidden; }
        .printable-receipt, .printable-receipt * { visibility: visible; }
        .printable-receipt { position: absolute; left: 0; top: 0; width: 100%; border: none !important; box-shadow: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# Main Database Initializer
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = []

# App Header Title
st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# Tab Navigation
tab1, tab2, tab3 = st.tabs([
    "🔍 लाइव स्क्रीन (View Database)", 
    "➕ नई प्रॉपर्टी जोड़ें", 
    "💳 डिजिटल बिलिंग (Billing)"
])

# TAB 1: VIEW & DELETE PROPERTIES
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    # Loop using index to safely remove/delete item
    for index, p in enumerate(list(st.session_state.properties)):
        col_info, col_del = st.columns([4, 1])
        
        with col_info:
            st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
            st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}")
            st.write(f"👤 मालिक: {p['owner']}")
            
            msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
            wa_url = f"https://wa.me/918109471091?text={msg.replace(' ', '%20')}"
            st.markdown(f"[💬 WhatsApp पर विवरण भेजें]({wa_url})")
            
        with col_del:
            st.write(" ")
            st.write(" ")
            if st.button("❌ डिलीट करें", key=f"delete_btn_{p['id']}_{index}"):
                st.session_state.properties.pop(index)
                st.warning(f"🗑️ {p['name']} को सफलतापूर्वक हटा दिया गया है!")
                st.rerun()
                
        st.write("---")

# TAB 2: ADD NEW PROPERTY WITH STABLE BUTTON
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("property_addition_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        submit_btn = st.form_submit_button("☁️ सुरक्षित लाइव सेव करें")
        if submit_btn:
            if n and r:
                new_id = f"PROP-{random.randint(400, 999)}"
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o
                })
                st.success(f"🎉 प्रॉपर्टी '{n}' डेटाबेस में लाइव जोड़ दी गई है!")
                st.balloons()
                st.rerun()
            else:
                st.error("कृपया प्रॉपर्टी का नाम और कीमत जरूर भरें!")

# TAB 3: BILLING ENGINE WITH DIRECT PRINT FUNCTION
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    col_l, col_r = st.columns(2)
    
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value="maa proprey")
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value="chatarkhar")
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", value="umasankar")
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value="8109471091")

    with col_r:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=20000000, step=5000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=0, step=1000)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=100000, step=5000)

    # Computations
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write("---")
    
    # Store dynamic receipt block in session memory to prevent wipeout on clicking print
    if 'active_bill' not in st.session_state:
        st.session_state.active_bill = None

    if st.button("✨ डिजिटल रसीद तैयार करें"):
        if b_name == "":
            st.error("कृपया बिल जनरेट करने के लिए प्रॉपर्टी का नाम लिखें!")
        else:
            inv_id = f"INV-{random.randint(3000, 3999)}"
            st.session_state.active_bill = {
                "id": inv_id, "date": current_date, "time": current_time,
                "b_name": b_name, "b_loc": b_loc, "c_name": c_name, "c_phone": c_phone,
                "base": base_price, "disc": disc, "total": final_total, "adv": adv, "due": pending_amount
            }
            # Append ledger history register
            st.session_state.bill_records.append({
                "रसीद ID": inv_id, "तारीख": current_date, "प्रॉपर्टी": b_name, "कस्टमर": c_name, "बकाया राशि": pending_amount
            })
            st.success("✅ डिजिटल रसीद जनरेट हो चुकी है! नीचे प्रिंट आउट बटन दबाएं।")

    # Display receipt if session state data is present
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        
        # Asli Print Window Trigger Button (Browser native print call)
        st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
                <button onclick="window.print()" style="
                    background-color: #00ffcc; 
                    color: #000000; 
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 12px 35px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer;
                    box-shadow: 0 4px 10px rgba(0,255,204,0.4);
                ">🖨️ Print Receipt (रसीद पेपर प्रिंट आउट निकालें)</button>
            </div>
        """, unsafe_allow_html=True)
        
        # Render the accurate premium white invoice matching your design
        st.markdown(f"""
        <div class="invoice-card printable-receipt">
            <div style="text-align: center; border-bottom: 2px solid #000000; padding-bottom: 6px; margin-bottom: 15px;">
                <h2 style="margin: 0; font-size: 24px;"><b>|| माँ प्रॉपर्टीज ||</b></h2>
                <p style="margin: 4px 0 0 0; font-size: 13px;">डिजिटल रसीद / इनवॉइस कॉपी</p>
            </div>
            
            <table style="width: 100%; font-size: 13px; margin-bottom: 8px;">
                <tr><td><b>INVOICE NO:</b> {rb['id']}</td><td style="text-align: right;"><b>DATE:</b> {rb['date']}</td></tr>
                <tr><td><b>STATUS:</b> SAFE RECORDED</td><td style="text-align: right;"><b>TIME:</b> {rb['time']}</td></tr>
            </table>
            
            <hr style="border-top: 1px dashed #000000; margin: 10px 0;">
            
            <table style="width: 100%; font-size: 14px; line-height: 1.7;">
                <tr><td style="width: 35%;"><b>🏢 प्रॉपर्टी का नाम:</b></td><td><b>{rb['b_name']}</b></td></tr>
                <tr><td><b>📍 पता / लोकेशन:</b></td><td>{rb['b_loc']}</td></tr>
                <tr><td><b>👤 ग्राहक का नाम:</b></td><td>{rb['c_name']}</td></tr>
                <tr><td><b>📞 मोबाइल नंबर:</b></td><td>{rb['c_phone']}</td></tr>
            </table>
            
            <hr style="border-top: 1px dashed #000000; margin: 10px 0;">
            
            <table style="width: 10
         
