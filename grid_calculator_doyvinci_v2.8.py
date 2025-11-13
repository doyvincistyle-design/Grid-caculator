import streamlit as st
import pandas as pd
from math import floor

st.set_page_config(page_title="Grid Calculator by Doyvinci", page_icon="💰", layout="centered")

# --- CSS Styling ---
st.markdown("""
<style>
body {background-color: #ffffff;}
.main {background-color: #ffffff;}
header {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 0rem;}
.header {text-align: center; margin-bottom: 30px;}
.title {font-size:38px; font-weight:700; color:#111827; margin:0;}
.subtitle {font-size:15px; color:#6b7280; margin-top:4px;}
.card {background: #ffffff; border-radius:14px; padding:24px; box-shadow: 0 2px 8px rgba(15,23,42,0.08);}
.footer {text-align:center; color:#374151; margin-top:40px; padding-top:16px; border-top:1px solid #e6e9ee;}
.social img {width:30px; height:30px; margin:0 8px; vertical-align:middle;}
.social a {text-decoration:none; color:#111827; font-weight:600; margin:0 6px;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    """
    <div class="header">
        <p style="font-size:70px;">💰</p>
        <p class="title">Grid Calculator <span style="font-weight:500;">by Doyvinci</span></p>
        <p class="subtitle">คำนวณทุนที่ต้องใช้สำหรับการเปิด Buy Grid ทองคำ (XAUUSD)</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Input Form ---
st.markdown('<div class="card">', unsafe_allow_html=True)

start_price = st.number_input("🎯 ราคาเริ่มต้นเปิด Buy ($)", value=4200.0, step=1.0)
end_price = st.number_input("💪 ราคาที่อยากทนได้ ($)", value=3500.0, step=1.0)
step = st.number_input("📏 เปิดทุกๆกี่ $", value=1.0, step=0.5)
lot_size = st.number_input("📊 ขนาด Lot ต่อไม้ (lot)", value=0.02, step=0.01)

calculate = st.button("คำนวณทุน (Calculate)")

if calculate:
    if end_price >= start_price:
        st.error("ราคาที่อยากทนต้องน้อยกว่าราคาเริ่มต้น (end < start)")
    elif step <= 0 or lot_size <= 0:
        st.error("ค่า Step และ Lot ต้องมากกว่า 0")
    else:
        # --- กำหนด contract size สำหรับ Standard ---
        contract_size = 100  # 1 lot Standard = 100 oz
        currency_unit = "USD"

        orders = floor((start_price - end_price) / step)

        df_data = []
        total_loss = 0.0

        # --- คำนวณขาดทุนแต่ละไม้ ---
        for i in range(orders):
            price_current = start_price - step * i
            # ขาดทุนแต่ละไม้ = -(ราคาเปิด - ราคาสุดท้าย) * contract_size * lot_size
            loss_current = -(price_current - end_price) * contract_size * lot_size
            total_loss += loss_current
            df_data.append({
                "ไม้ที่": i + 1,
                "ราคาทอง ($)": round(price_current, 2),
                f"ขาดทุน ({currency_unit})": round(loss_current, 2)
            })

        df = pd.DataFrame(df_data)

        st.markdown("### 📊 ตารางขาดทุนแต่ละไม้")
        st.dataframe(df, use_container_width=True)

        st.markdown(f"💰 ขาดทุนสะสมทั้งหมด ≈ {total_loss:,.2f} {currency_unit}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer แบบเดิม ---
st.markdown("""
<div class="footer">
    <p>Contact</p>
    <div class="social">
        <a href="https://www.facebook.com/profile.php?id=61581992519734" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png"> เทรดทองคำแบบ Grid by Doyvinci
        </a><br>
        <a href="https://www.instagram.com/doyvinci" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png"> @doyvinci
        </a><br>
        <a href="https://www.youtube.com/@DoyvinciStyle" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png"> เทรดแบบ Grid by Doyvinci
        </a>
    </div>
</div>
""", unsafe_allow_html=True)