import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="मां配置 प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. डिजिटल रसीद के लिए स्पेशल प्रिंटर स्टाइलिंग (CSS)
# यह कोड प्रिंटर को बताता है कि रसीद के अलावा स्क्रीन की बाकी चीजें कागज़ पर न छापें
st.markdown("""
<style>
    /* जब सामान्य स्क्रीन पर देखें तो रसीद कैसी दिखे */
    .digital-bill-box {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border: 2px solid #333333;
        border-radius: 8px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        max-width: 600px;
        margin: 20px auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 🖨️ प्रिंटर कमांड चालू होते ही ये नियम काम करेंगे */
    @media print {
        /* पूरी स्क्रीन के बटन, हेडर, टैब सबको छुपा दो */
        body * {
            visibility: hidden;
            background: white !important;
            color: black !important;
        }
        /* सिर्फ रसीद वाले मुख्य बॉक्स को स्क्रीन पर दिखाओ और प्रिंट करो */
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
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = [
        {"bill_id": "INV-3012", "date": "26-05-2026", "prop_name": "Maa Property", "location": "Chatarkhar", "cust_name": "Umasankar", "phone": "8109471091", "base": 20000000, "disc": 0, "adv": 100000, "due": 19900000}
    ]

if 'active_bill' not in st.session_state:
    st.session_state.active_bill = None

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# मुख्य ऐप टाइटल
st.title("⚡ मां प्रॉपर्टी डिजिटल क्लाउड ऐप 2026")
st.write("---")

tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (Properties)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग एवं रिकॉर्ड रजिस्टर"])

# ==================== टैब 1: लाइव प्रॉपर्टी लिस्ट ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    props_list = list(st.session_state.properties)
    for index, p in enumerate(props_list):
        col_info, col_del = st.columns([4, 1])
        with col_info:
            st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
            st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{p['rate']}")
            st.write(f"👤 मालिक: {p['owner']}")
            
            msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} में इंटरेस्ट है।"
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
    with st.form("property_form_v2", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया")
        r = st.text_input("कुल कीमत (सिर्फ नंबर)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        if st.form_submit_button("☁️ सुरक्षित लाइव सेव करें"):
            if n and r:
                new_id = "PROP-" + str(random.randint(400, 999))
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o
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
        default_base, default_disc, default_adv = int(edit_data["base"]), int(edit_data["disc"]), int(edit_data["adv"])
    else:
        default_bname, default_bloc, default_cname, default_cphone = "maa proprey", "chatarkhar", "umasankar", "8109471091"
        default_base, default_disc, default_adv = 20000000, 0, 100000

    col_l, col_r = st.columns(2)
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value=default_bname)
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value=default_bloc)
        c_name = st.text_input("3. ग्राहक का नाम", value=default_cname)
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value=default_cphone)
    with col_r:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=default_base)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=default_disc)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=default_adv)

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
                    "prop_name": b_name, "location": b_loc, "cust_name": c_name, "phone": c_phone,
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
                        "prop_name": b_name, "location": b_loc, "cust_name": c_name, "phone": c_phone,
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

    # ==================== 100% एकदम डिजिटल और साफ प्रिंट आउट रसीद बॉक्स ====================
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.write("---")
        st.write("### 🧾 प्रिंट प्रीव्यू (यह रसीद एकदम साफ़ कागज़ पर निकलेगी)")
        
        # 🖨️ डायरेक्ट प्रिंट करने का बटन
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 15px 30px; border: 2px solid black; border-radius: 6px; cursor: pointer; width: 100%; font-size: 18px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">🖨️ यहाँ क्लिक करके तुरंत असली डिजिटल रसीद प्रिंट करें</button>', unsafe_allow_html=True)
        
        # यह वो एचटीएमएल (HTML) बॉक्स है जो प्रिंटर पर एकदम डिजिटल स्टाइल में छपेगा
        receipt_html = f"""
        <div class="digital-bill-box printable-bill-area">
            <div style="text-align: center; border-bottom: 3px double #000000; padding-bottom: 10px; margin-bottom: 15px;">
                <h1 style="margin: 0; font-size: 26px; color: #000000; font-weight: bold; letter-spacing: 1px;">|| माँ प्रॉपर्टीज ||</h1>
                <p style="margin: 5px 0 0 0; font-size: 14px; color: #555555; font-style: italic;">रियल एस्टेट एवं डिजिटल बिलिंग सॉल्यूशंस</p>
            </div>
            
            <table style="width: 100%; font-size: 14px; margin-bottom: 15px; color: #000000;">
                <tr>
                    <td><b>इनवॉइस नंबर:</b> {rb['bill_id']}</td>
                    <td style="text-align: right;"><b>दिनांक:</b> {rb['date']}</td>
                </tr>
            </table>
            
            <div style="background-color: #f9f9f9; padding: 12px; border-radius: 5px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
                <table style="width: 100%; font-size: 14px; line-height: 1.8; color: #000000;">
                    <tr><td style="width: 35%;"><b>🏢 प्रॉपर्टी का नाम:</b></td><td><b>{rb['prop_name']}</b></td></tr>
                    <tr><td><b>📍 लोकेशन / पता:</b></td><td>{rb['location']}</td></tr>
                    <tr><td><b>👤 ग्राहक का नाम:</b></td><td>{rb['cust_name']}</td></tr>
                    <tr><td><b>📞 मोबाइल नंबर:</b></td><td>{rb['phone']}</td></tr>
                </table>
            </div>
            
            <table style="width: 100%; font-size: 14px; border-collapse: collapse; color: #000000;">
                <thead>
                    <tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000; font-weight: bold; background-color: #f0f0f0;">
                        <td style="padding: 8px 5px;">वित्तीय विवरण (Particulars)</td>
                        <td style="text-align: right; padding: 8px 5px;">राशि (Amount)</td>
                    </tr>
                </thead>
                <tbody>
                    <tr><td style="padding: 8px 5px;">मूल सौदा मूल्य (Base Price)</td><td style="text-align: right; padding: 8px 5px;">₹{rb['base']:,}.00</td></tr>
                    <tr><td style="padding: 8px 5px; color: #555555;">विशेष व्यापार छूट (Discount)</td><td style="text-align: right; padding: 8px 5px; color: #555555;">- ₹{rb['disc']:,}.00</td></tr>
                    <tr style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; font-weight: bold;">
                        <td style="padding: 8px 5px;">कुल फाइनल सौदा मूल्य</td>
                        <td style="text-align: right; padding: 8px 5px;">₹{rb['base'] - rb['disc']:,}.00</td>
                    </tr>
                    <tr><td style="padding: 8px 5px; color: green;"><b>प्राप्त एडवांस (बयाना राशि)</b></td><td style="text-align: right; padding: 8px 5px; color: green;"><b>₹{rb['adv']:,}.00</b></td></tr>
                    <tr style="border-top: 2px solid #000000; font-weight: bold; font-size: 16px; background-color: #f5f5f5;">
                        <td style="padding: 10px 5px; color: #cc0000;">🔴 कुल बकाया राशि (DUE)</td>
                        <td style="text-align: right; padding: 10px 5px; color: #cc0000;">₹{rb['due']:,}.00</td>
                    </tr>
                </tbody>
            </table>
            
            <div style="margin-top: 35px; text-align: center; font-size: 12px; border-top: 1px dashed #000000; padding-top: 10px; color: #555555;">
                <p>यह एक कंप्यूटर जनरेटेड डिजिटल रसीद है।<br><b>मां प्रॉपर्टी क्लाउड सिस्टम्स 2026 द्वारा सत्यापित</b></p>
            </div>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

    # ==================== सुरक्षित बिल रिकॉर्ड रजिस्टर ====================
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर")
    st.write("यहाँ से आप पुराने बिलों को कभी भी मैनेज (एडिट/डिलीट) कर सकते हैं:")
    
    records_list = list(st.session_state.bill_records)
    if len(records_list) > 0:
        for r_idx, r_data in enumerate(records_list):
            col_rec_info, col_rec_edit, col_rec_del = st.columns([3, 1, 1])
            
            with col_rec_info:
                st.code(f"🆔 {r_data['bill_id']} | 📅 {r_data['date']} | 👤 {r_data['cust_name']} | 🏢 {r_data['prop_name']} | 🔴 बकाया: ₹{r_data['due']:,}")
            
            with col_rec_edit:
                if st.button("✏️ एडिट करें", key=f"btn_edit_rec_{r_data['bill_id']}_{r_idx}"):
                    st.session_state.edit_index = r_idx
                    st.rerun()
                    
            with col_rec_del:
                if st.button("🗑️ डिलीट", key=f"btn_del_rec_{r_data['bill_id']}_{r_idx}"):
                    st.session_state.bill_records.pop(r_idx)
                    if st.session_state.active_bill and st.session_state.active_bill["bill_id"] == r_data["bill_id"]:
                        st.session_state.active_bill = None
                    st.warning("🗑️ रसीद रिकॉर्ड से हमेशा के लिए हटा दी गई है!")
                    st.rerun()
    else:
        st.write("अभी रजिस्टर में कोई बिल सुरक्षित नहीं है।")
