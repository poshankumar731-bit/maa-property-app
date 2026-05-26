import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="Maa Property Digital App 2026", layout="wide")

# 2. वीआईपी डिजिटल इंग्लिश रसीद के लिए स्पेशल प्रिंटर CSS
st.markdown("""
<style>
    .digital-bill-box {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border: 2px solid #111111;
        border-radius: 8px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        max-width: 650px;
        margin: 20px auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    @media print {
        body * {
            visibility: hidden;
            background: white !important;
            color: black !important;
        }
        .printable-bill-area, .printable-bill-area * {
            visibility: visible;
        }
        .printable-bill-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            border: none !important;
            box-shadow: none !important;
            padding: 0px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 3. सुरक्षित डेटाबेस मेमोरी लॉक
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "SAI RESIDENCY", "type": "Plot", "area": "1200 SqFt", "rate": "2500000", "location": "SECTOR 15, LUCKNOW", "owner": "RAM KUMAR"},
        {"id": "PROP-356", "name": "CHATARKHAR LAND", "type": "Plot", "area": "87200", "rate": "1600", "location": "CHATARKHAR", "owner": "SELF OWNER"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = [
        {"bill_id": "INV-3012", "date": "26-05-2026", "prop_name": "MAA PROPERTY", "location": "CHATARKHAR", "cust_name": "UMASANKAR", "phone": "8109471091", "seller_name": "MAA PROPERTY OWNER", "base": 20000000, "disc": 0, "adv": 100000, "due": 19900000}
    ]

if 'active_bill' not in st.session_state:
    st.session_state.active_bill = None

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None


# ==================== 🔐 सुरक्षित मोबाइल लॉगिन स्क्रीन गेटवे ====================
if not st.session_state.logged_in:
    st.subheader("🔐 मां प्रॉपर्टीज डिजिटल क्लाउड - लॉगिन गेटवे")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("💡 सिक्योरिटी नोट: सुरक्षित लॉगिन के लिए अपना रजिस्टर्ड मोबाइल नंबर दर्ज करें।")
        mobile = st.text_input("📱 अपना मोबाइल नंबर दर्ज करें", max_chars=10, placeholder="91XXXXXXXX")
        otp_input = st.text_input("🔑 4-अंकों का OTP दर्ज करें (सुरक्षित मास्टर OTP: 1234 डालें)", type="password", max_chars=4)
        
        st.write(" ")
        if st.button("🔓 ऐप में सुरक्षित लॉगिन करें", type="primary"):
            if len(mobile) == 10 and otp_input == "1234":
                st.session_state.logged_in = True
                st.success("🎉 लॉगिन सफल! ऐप लोड हो रहा है...")
                st.rerun()
            elif len(mobile) != 10:
                st.error("❌ कृपया सही 10 अंकों का मोबाइल नंबर डालें!")
            else:
                st.error("❌ गलत OTP! कृपया सही सिक्योरिटी पिन दर्ज करें।")
    st.stop()


# ==================== 🏢 लॉगिन होने के बाद मुख्य ऐप ====================
col_title, col_logout = st.columns([5, 1])
with col_title:
    st.title("⚡ मां प्रॉपर्टी डिजिटल क्लाउड ऐप 2026")
with col_logout:
    st.write(" ")
    if st.button("🔒 लॉगआउट (Exit)"):
        st.session_state.logged_in = False
        st.rerun()

st.write("---")

tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (View Database)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग और रिकॉर्ड रजिस्टर"])

# ==================== टैब 1: लाइव प्रॉपर्टीज ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    props_list = list(st.session_state.properties)
    for index, p in enumerate(props_list):
        col_info, col_del = st.columns([4, 1])
        with col_info:
            st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
            st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{p['rate']}")
            st.write(f"👤 मालिक/विक्रेता: {p['owner']}")
            
            msg = f"Hello, I am interested in your property: {p['name']}."
            wa_url = "https://wa.me/918109471091?text=" + msg.replace(" ", "%20")
            st.markdown(f"[💬 WhatsApp पर विवरण भेजें]({wa_url})")
            
        with col_del:
            st.write(" ")
            st.write(" ")
            if st.button("❌ प्रॉपर्टी हटाएँ", key=f"del_prop_{index}"):
                st.session_state.properties.pop(index)
                st.warning("🗑️ प्रॉपर्टी हटा दी गई है!")
                st.rerun()
        st.write("---")

# ==================== टैब 2: नई प्रॉपर्टी एंट्री ====================
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("property_form_final", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया")
        r = st.text_input("कुल कीमत (सिर्फ नंबर)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक / विक्रेता का नाम")
        
        if st.form_submit_button("☁️ सुरक्षित लाइव सेव करें"):
            if n and r:
                new_id = "PROP-" + str(random.randint(400, 999))
                st.session_state.properties.append({
                    "id": new_id, 
                    "name": str(n).upper(), 
                    "type": t, 
                    "area": str(a), 
                    "rate": str(r), 
                    "location": str(l).upper(), 
                    "owner": str(o).upper()
                })
                st.success("🎉 सफलतापूर्वक लाइव सुरक्षित कर दी गई है!")
                st.rerun()

# ==================== टैब 3: डिजिटल बिलिंग और सुरक्षित रिकॉर्ड रजिस्टर ====================
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    is_edit = st.session_state.edit_index is not None
    if is_edit:
        st.warning("⚠️ आप अभी रिकॉर्ड रजिस्टर में पुराने बिल को एडिट कर रहे हैं!")
        edit_data = st.session_state.bill_records[st.session_state.edit_index]
        default_bname, default_bloc, default_cname, default_cphone = edit_data["prop_name"], edit_data["location"], edit_data["cust_name"], edit_data["phone"]
        default_sname = edit_data.get("seller_name", "MAA PROPERTIES")
        default_base, default_disc, default_adv = int(edit_data["base"]), int(edit_data["disc"]), int(edit_data["adv"])
    else:
        default_bname, default_bloc, default_cname, default_cphone = "MAA PROPERTY", "CHATARKHAR", "UMASANKAR", "8109471091"
        default_sname = "SELF OWNER"
        default_base, default_disc, default_adv = 20000000, 0, 100000

    col_l, col_r = st.columns(2)
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी का नाम (Property Name)", value=default_bname)
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value=default_bloc)
        c_name = st.text_input("3. खरीदार/क्रेता का नाम (Buyer Name)", value=default_cname)
        c_phone = st.text_input("4. खरीदार का मोबाइल नंबर", value=default_cphone)
        s_name = st.text_input("5. विक्रेता/मालिक का नाम (Seller Name)", value=default_sname)

    with col_r:
        base_price = st.number_input("6. मूल सौदा राशि (₹)", min_value=0, value=default_base)
        disc = st.number_input("7. डिस्काउंट / छूट (₹)", min_value=0, value=default_disc)
        adv = st.number_input("8. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=default_adv)

    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    
    st.write(" ")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if is_edit:
            if st.button("💾 एडिट किया हुआ बिल अपडेट करें", type="primary"):
                idx = st.session_state.edit_index
                updated_record = {
                    "bill_id": edit_data["bill_id"], "date": edit_data["date"],
                    "prop_name": str(b_name).upper(), "location": str(b_loc).upper(), 
                    "cust_name": str(c_name).upper(), "phone": c_phone, "seller_name": str(s_name).upper(),
                    "base": base_price, "disc": disc, "adv": adv, "due": pending_amount
                }
                st.session_state.bill_records[idx] = updated_record
                st.session_state.active_bill = updated_record
                st.session_state.edit_index = None
                st.success("✅ रिकॉर्ड सफलतापूर्वक अपडेट हो गया!")
                st.rerun()
        else:
            if st.button("✨ नई डिजिटल रसीद तैयार करें", type="primary"):
                if b_name == "":
                    st.error("कृपया प्रॉपर्टी का नाम लिखें!")
                else:
                    inv_id = "INV-" + str(random.randint(3000, 3999))
                    new_bill = {
                        "bill_id": inv_id, "date": current_date,
                        "prop_name": str(b_name).upper(), "location": str(b_loc).upper(), 
                        "cust_name": str(c_name).upper(), "phone": c_phone, "seller_name": str(s_name).upper(),
                        "base": base_price, "disc": disc, "adv": adv, "due": pending_amount
                    }
                    st.session_state.active_bill = new_bill
                    st.session_state.bill_records.append(new_bill)
                    st.success("✅ नई डिजिटल रसीद रजिस्टर में सुरक्षित हो चुकी है!")

    with col_btn2:
        if is_edit:
            if st.button("❌ बदलाव रद्द करें"):
                st.session_state.edit_index = None
                st.rerun()

    # ==================== 🖨️ 100% शुद्ध अंग्रेजी डिजिटल ऑटो-कैपिटल रसीद ====================
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.write("---")
        st.write("### 🧾 Invoice Preview (यह रसीद एकदम साफ कागज़ पर अंग्रेजी में निकलेगी)")
        
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 16px 30px; border: 2px solid black; border-radius: 6px; cursor: pointer; width: 100%; font-size: 18px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">🖨️ Click Here to Print Original Invoice</button>', unsafe_allow_html=True)
        
        receipt_html = f"""
        <div class="digital-bill-box printable-bill-area">
            <div style="text-align: center; border-bottom: 3px double #000000; padding-bottom: 10px; margin-bottom: 15px;">
                <h1 style="margin: 0; font-size: 28px; color: #000000; font-weight: bold; letter-spacing: 1px;">MAA PROPERTIES</h1>
                <p style="margin: 5px 0 0 0; font-size: 13px; color: #555555; font-style: italic; letter-spacing: 0.5px;">Real Estate Consultants & Digital Billing Solutions</p>
            </div>
            
            <table style="width: 100%; font-size: 14px; margin-bottom: 20px; color: #000000; font-family: Arial, sans-serif;">
                <tr>
                    <td><b>Invoice No:</b> {rb['bill_id']}</td>
                    <td style="text-align: right;"><b>Date:</b> {rb['date']}</td>
                </tr>
            </table>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0; margin-bottom: 25px;">
                <table style="width: 100%; font-size: 14px; line-height: 1.9; color: #000000; font-family: Arial, sans-serif;">
                    <tr><td style="width: 35%;"><b>Property Name:</b></td><td><b>{str(rb['prop_name']).upper()}</b></td></tr>
                    <tr><td><b>Location / Address:</b></td><td>{str(rb['location']).upper()}</td></tr>
                    <tr><td><b>Buyer Name:</b></td><td><b>{str(rb['cust_name']).upper()}</b></td></tr>
                    <tr><td><b>Mobile Number:</b></td><td>{rb['phone']}</td></tr>
                    <tr><td><b>Seller Name:</b></td><td><b>{str(rb['seller_name']).upper()}</b></td></tr>
                </table>
            </div>
            
            <table style="width: 100%; font-size: 14px; border-collapse: collapse; color: #000000; font-family: Arial, sans-serif;">
                <thead>
                    <tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000; font-weight: bold; background-color: #f0f0f0;">
                        <td style="padding: 10px 5px;">Particulars</td>
                        <td style="text-align: right; padding: 10px 5px;">Amount (INR)</td>
                    </tr>
                </thead>
                <tbody>
                    <tr><td style="padding: 10px 5px;">Base Property Deal Price</td><td style="text-align: right; padding: 10px 5px;">Ref. {int(rb['base']):,}.00</td></tr>
                    <tr><td style="padding: 10px 5px; color: #555555;">Special Discount Given</td><td style="text-align: right; padding: 10px 5px; color: #555555;">- Ref. {int(rb['disc']):,}.00</td></tr>
                    <tr style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; font-weight: bold;">
                        <td style="padding: 10px 5px;">Net Deal Amount</td>
                        <td style="text-align: right; padding: 10px 5px;">Ref. {int(rb['base']) - int(rb['disc']):,}.00</td>
                    </tr>
                    <tr><td style="padding: 10px 5px; color: green;"><b>Advance Amount Received (Bayana)</b></td><td style="text-align: right; padding: 10px 5px; color: green;"><b>Ref. {int(rb['adv']):,}.00</b></td></tr>
                    <tr style="border-top: 2px solid #000000; font-weight: bold; font-size: 16px; background-color: #f5f5f5;">
                        <td style="padding: 12px 5px; color: #cc0000;">TOTAL PENDING DUE</td>
                        <td style="text-align: right; padding: 12px 5px; color: #cc0000;"><b>Ref. {int(rb['due']):,}.00</b></td>
                    </tr>
                </tbody>
            </table>
            
            <div style="margin-top: 60px; font-size: 14px; color: #000000; width: 100%; font-family: Arial, sans-serif;">
                <table style="width: 100%;">
                    <tr>
                        <td style="width: 50%; text-align: left;"><br><br>____________________<br><b>Buyer's Signature</b></td>
                        <td style="width: 50%; text-align: right;"><br><br>____________________<br><b>Authorized Signatory</b></td>
                    </tr>
                </table>
            </div>
            
            <div style="margin-top: 40px; text-align: center; font-size: 11px; border-top: 1px dashed #000000; padding-top: 10px; color: #666666;">
                <p>This is a computer-generated digital invoice.<br><b>Verified by Maa Property Cloud Systems 2026</b></p>
            </div>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

    # ==================== सुरक्षित बिल रिकॉर्ड रजिस्टर ====================
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर")
    
    records_list = list(st.session_state.bill_records)
    if len(records_list) > 0:
        for r_idx, r_data in enumerate(records_list):
            col_rec_info, col_rec_edit, col_rec_del = st.columns([3, 1, 1])
            
            with col_rec_info:
                st.code(f"🆔 {r_data['bill_id']} | 📅 {r_data['date']} | 👤 Buyer: {str(r_data['cust_name']).upper()} | 🏢 {str(r_data['prop_name']).upper()} | 🔴 Due: Ref. {int(r_data['due']):,}")
            
            with col_rec_edit:
                if st.button("✏️ एडिट", key=f"btn_edit_rec_{r_data['bill_id']}_{r_idx}"):
                    st.session_state.edit_index = r_idx
                    st.rerun()
                    
            with col_rec_del:
                if st.button("🗑️ डिलीट", key=f"btn_del_rec_{r_data['bill_id']}_{r_idx}"):
                    st.session_state.bill_records.pop(r_idx)
                    if st.session_state.active_bill and st.session_state.active_bill["bill_id"] == r_data["bill_id"]:
                        st.session_state.active_bill = None
                    st.warning("🗑️ रसीद रिकॉर्ड से हटा दी गई है!")
                    st.rerun()
    else:
        st.write("अभी रजिस्टर में कोई बिल सुरक्षित नहीं है।")
