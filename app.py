import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="AI Fiyat Eksperi", page_icon="🤖")

st.title("🤖 AI Fiyat Eksperi")
st.write("Taşınmaz ve Araç Değerleme Asistanı")

tab1, tab2 = st.tabs(["🚗 Araba Değerleme", "🏠 Ev Değerleme"])

with tab1:
    st.header("Araba Bilgileri")
    yil = st.number_input("Model Yılı", min_value=1990, max_value=2026, value=2020)
    km = st.number_input("Kilometre", min_value=0, value=50000)
    hasar = st.number_input("Hasar Kaydı (TL)", min_value=0, value=0)
    boya = st.slider("Boya/Değişen Parça Sayısı", 0, 13, 0)
    lastik = st.selectbox("Lastik Durumu", ["İyi", "Değişim Lazım"])
    
    if st.button("Araba Fiyatı Hesapla"):
        fiyat = 1000000 - ((2026 - yil) * 45000) - (km * 0.6) - hasar - (boya * 15000)
        if lastik == "Değişim Lazım": fiyat -= 15000
        st.success(f"Tahmini Değer: {round(max(fiyat, 50000), 2):,} TL")

with tab2:
    st.header("Ev Bilgileri")
    bolge = st.selectbox("Bölge Seçiniz", ["Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu"])
    m2 = st.number_input("Metrekare (m2)", min_value=20, value=100)
    kat = st.number_input("Kat No", value=2)
    gunes = st.radio("Güneş Görüyor mu?", ["Evet", "Hayır"])
    
    if st.button("Ev Fiyatı Hesapla"):
        katsayilar = {"Marmara": 2.5, "Ege": 2.1, "Akdeniz": 1.9, "İç Anadolu": 1.6, "Karadeniz": 1.5, "Doğu Anadolu": 1.2}
        fiyat = m2 * 18000 * katsayilar[bolge]
        if kat == 0: fiyat *= 0.90
        if gunes == "Evet": fiyat *= 1.10
        st.success(f"Tahmini Değer: {round(max(fiyat, 350000), 2):,} TL")