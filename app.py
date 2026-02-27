import streamlit as st

st.set_page_config(page_title="AI Fiyat Eksperi - Pro", layout="wide")
st.title("🤖 Yapay Zeka Fiyat Eksperi (Sahibinden Modu)")

tab1, tab2 = st.tabs(["🚗 Araba Değerleme", "🏠 Ev Değerleme"])

with tab1:
    st.header("Araç Detaylarını İşaretleyiniz")
    c1, c2 = st.columns(2)
    
    with c1:
        segment = st.selectbox("Marka Grubu", ["Lüks (BMW, Mercedes, Audi)", "Orta (Toyota, VW, Honda)", "Ekonomik (Fiat, Renault, Dacia)"])
        kasa = st.radio("Kasa Tipi", ["Otomobil", "SUV / 4x4"])
        vites = st.radio("Şanzıman", ["Otomatik", "Manuel"])
        
        st.subheader("Motor Gücü (HP)")
        hp_secenek = st.radio("HP Aralığı", ["50 HP'ye kadar", "51 - 75 HP", "76 - 100 HP", "101 - 125 HP", "126 - 150 HP", "151 HP ve üzeri"], index=2)

    with c2:
        st.subheader("Motor Hacmi (cm³)")
        hacim_secenek = st.radio("Hacim Aralığı", ["1300 cm³'e kadar", "1301 - 1600 cm³", "1601 - 1800 cm³", "1801 - 2000 cm³", "2001 - 2500 cm³", "2501 cm³ ve üzeri"], index=1)
        
        yil = st.selectbox("Model Yılı", list(range(2026, 1999, -1)))
        km = st.number_input("Kilometre", 0, 1000000, 100000)

    st.subheader("Hasar ve Ekspertiz")
    e1, e2 = st.columns(2)
    with e1:
        tramer = st.number_input("Tramer Kaydı (TL)", 0, 1000000, 0)
    with e2:
        parcalar = st.multiselect("Boyalı/Değişen Parçalar", ["Kaput", "Tavan", "Bagaj", "Kapılar", "Çamurluklar"])

    if st.button("Piyasayı Analiz Et"):
        # Güncel 2026 "Sahibinden" Fiyat Mantığı
        baz = 4500000 if "Lüks" in segment else 1800000 if "Orta" in segment else 1100000
        
        # Seçilen aralıklara göre fiyat çarpanları
        hacim_mult = 1.4 if "2001" in hacim_secenek or "2501" in hacim_secenek else 1.15 if "1601" in hacim_secenek else 1.0
        hp_mult = 1.3 if "151" in hp_secenek else 1.1 if "101" in hp_secenek else 0.9
        
        tahmin = (baz * hacim_mult * hp_mult)
        if kasa == "SUV / 4x4": tahmin *= 1.35
        if vites == "Otomatik": tahmin *= 1.18
        
        # Yaş ve KM kaybı
        tahmin -= (2026 - yil) * (tahmin * 0.04)
        tahmin -= (km * 2)
        tahmin -= (tramer * 1.2) + (len(parcalar) * 35000)
        
        st.success(f"🏁 Tahmini Piyasa Değeri: {max(tahmin, 400000):,.0f} TL")

with tab2:
    st.header("Mülk Detaylarını Seçiniz")
    m1, m2 = st.columns(2)
    with m1:
        m_tipi = st.selectbox("Konut Tipi", ["Daire", "Müstakil", "Villa", "Rezidans"])
        oda = st.select_slider("Oda Sayısı", options=["1+0", "1+1", "2+1", "3+1", "4+1", "5+1+"])
        bolge = st.selectbox("Bölge / Muhit", ["Bolu Merkez (Lüks)", "Bolu Merkez (Standart)", "Karabük Merkez", "Gelişmekte Olan Bölge"])
    
    with m2:
        m2_brut = st.number_input("Brüt m²", 40, 1000, 120)
        m2_net = st.number_input("Net m²", 35, 900, 105)
        b_yasi = st.number_input("Bina Yaşı", 0, 60, 0)
        cephe = st.radio("Cephe", ["Güney (Güneş Alan)", "Kuzey", "Doğu/Batı"])

    if st.button("Emlak Değerini Hesapla"):
        # 2026 Emlak Piyasası (Yüksek Fiyatlar)
        birim_m2 = 65000 if "Lüks" in bolge else 45000 if "Standart" in bolge else 35000
        if m_tipi == "Villa": birim_m2 *= 2.2
        if m_tipi == "Rezidans": birim_m2 *= 1.8
        
        tahmin_ev = (m2_net * birim_m2)
        if cephe == "Güney (Güneş Alan)": tahmin_ev *= 1.12
        if b_yasi == 0: tahmin_ev *= 1.30 # Sıfır bina primi
        
        st.success(f"🏠 Tahmini Konut Değeri: {tahmin_ev:,.0f} TL")