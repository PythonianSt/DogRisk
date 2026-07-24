import streamlit as st
import pydeck as pdk
from streamlit_geolocation import streamlit_geolocation


st.set_page_config(
    page_title="ตำแหน่งของท่าน",
    page_icon="📍",
    layout="wide",
)

st.title("📍 ตำแหน่งของท่าน")
st.write(
    "กดปุ่มด้านล่าง และอนุญาตให้เบราว์เซอร์เข้าถึงตำแหน่งของท่าน"
)

# ขอพิกัดจากอุปกรณ์ของผู้ใช้งาน
location = streamlit_geolocation()

# ค่าที่ได้ก่อนผู้ใช้กดปุ่มอาจเป็นข้อความหรือ dictionary ว่าง
if not isinstance(location, dict):
    st.info("กรุณากดปุ่มรับตำแหน่ง และเลือก Allow หรืออนุญาต")
    st.stop()

latitude = location.get("latitude")
longitude = location.get("longitude")
accuracy = location.get("accuracy")

if latitude is None or longitude is None:
    st.info("ยังไม่ได้รับตำแหน่ง กรุณากดปุ่มและอนุญาตการใช้ตำแหน่ง")
    st.stop()

# ข้อมูลจุดตำแหน่ง
map_data = [
    {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "label": "ท่านอยู่ที่นี่",
    }
]

# จุดวงกลม
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position="[longitude, latitude]",
    get_radius=12,
    radius_min_pixels=9,
    radius_max_pixels=18,
    get_fill_color=[220, 30, 30, 230],
    get_line_color=[255, 255, 255],
    line_width_min_pixels=3,
    stroked=True,
    filled=True,
    pickable=True,
)

# ข้อความเหนือจุด
text_layer = pdk.Layer(
    "TextLayer",
    data=map_data,
    get_position="[longitude, latitude]",
    get_text="label",
    get_size=18,
    get_color=[20, 20, 20],
    get_angle=0,
    get_text_anchor="'middle'",
    get_alignment_baseline="'bottom'",
    get_pixel_offset=[0, -18],
)

# กำหนดมุมมองแผนที่ให้ตรงกับตำแหน่งผู้ใช้
view_state = pdk.ViewState(
    latitude=float(latitude),
    longitude=float(longitude),
    zoom=17,
    pitch=0,
    bearing=0,
)

deck = pdk.Deck(
    layers=[point_layer, text_layer],
    initial_view_state=view_state,
    map_style="light",
    tooltip={
        "html": """
        <b>ท่านอยู่ที่นี่</b><br/>
        Latitude: {latitude}<br/>
        Longitude: {longitude}
        """,
        "style": {
            "backgroundColor": "white",
            "color": "black",
        },
    },
)

st.pydeck_chart(deck, width="stretch", height=600)

st.success("พบตำแหน่งของท่านแล้ว")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Latitude", f"{latitude:.6f}")

with col2:
    st.metric("Longitude", f"{longitude:.6f}")

with col3:
    if accuracy is not None:
        st.metric("ความคลาดเคลื่อนโดยประมาณ", f"{accuracy:.1f} เมตร")
    else:
        st.metric("ความคลาดเคลื่อน", "ไม่ทราบ")

st.caption(
    "พิกัดจะแม่นยำขึ้นเมื่อเปิด Location หรือ GPS "
    "และใช้งานในบริเวณที่รับสัญญาณได้ดี"
)