import streamlit as st
import time
from google import genai
from dotenv import load_dotenv
from PIL import Image

# --- 1. YETKİLENDİRME VE API AYARLARI ---
load_dotenv()
client = genai.Client()  # .env içindeki GOOGLE_API_KEY'i otomatik alır

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Cilt Analizi", page_icon="🐾", layout="wide")

# --- 2. GELİŞMİŞ CSS ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    [data-testid="stHeader"] {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stStatusWidget"] {display: none !important;}

    .stApp { background-color: #FAF3F0; } 

    html, body, [class*="st-"], p, h1, h2, h3, h4, h5, h6, span, label, div, li {
        color: #4A2E39 !important; 
        font-family: 'Segoe UI', sans-serif;
    }

    div.stFormSubmitButton > button, div.stButton > button {
        background-color: #C1D7AE !important; 
        color: #4A2E39 !important;
        border: 2px solid #A9C296 !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        width: 100% !important;
        transition: 0.3s !important;
    }

    .question-card {
        background-color: white; padding: 30px; border-radius: 25px;
        margin-bottom: 20px; border: 2px solid #FADADD;
        box-shadow: 0 4px 15px rgba(74, 46, 57, 0.05);
    }

    .sonuc-karti {
        background-color: white; padding: 25px; border-radius: 20px;
        margin-bottom: 20px; border-left: 10px solid #C1D7AE;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.05);
    }

    .sonuc-karti-riskli {
        background-color: white; padding: 25px; border-radius: 20px;
        margin-bottom: 20px; border: 3px solid #E57373 !important;
        border-left: 15px solid #E57373 !important;
    }

    .skor-kutusu {
        background-color: white; padding: 40px; border-radius: 30px;
        text-align: center; border: 3px solid #C1D7AE; margin-bottom: 30px;
    }
    .skor-deger {
        font-size: 90px !important; font-weight: 900 !important;
        color: #7FB069 !important; line-height: 1;
    }

    @keyframes pulse-block {
      0% { background-color: #FADADD; transform: scale(1); }
      50% { background-color: #C1D7AE; transform: scale(1.1); }
      100% { background-color: #FADADD; transform: scale(1); }
    }
    .loading-container {
      background-color: white; padding: 30px; border-radius: 25px;
      text-align: center; border: 1px solid #EADBC8;
    }
    .loading-block {
      width: 80px; height: 80px; border-radius: 20px;
      margin: 0 auto 15px auto; animation: pulse-block 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HAFIZA YÖNETİMİ ---
if 'test_bitti' not in st.session_state: st.session_state.test_bitti = False
if 'cilt_tipi' not in st.session_state: st.session_state.cilt_tipi = ""
if 'analiz_durumu' not in st.session_state: st.session_state.analiz_durumu = "bekliyor"
if 'kayitli_rapor' not in st.session_state: st.session_state.kayitli_rapor = ""
if 'last_fn' not in st.session_state: st.session_state.last_fn = None


def avatar_goster(durum, genislik=400):
    try:
        if durum in ["bekliyor", "analiz_ediyor"]:
            st.image("1.png", width=genislik)
        elif durum == "tamamlandi_uygun":
            st.image("2.png", width=genislik)
        elif durum == "tamamlandi_uygun_degil":
            st.image("3.png", width=genislik)
    except:
        st.info("Avatar görselleri bulunamadı.")


# --- EKRAN 1: ANKET ---
if not st.session_state.test_bitti:
    col_kedi, col_title = st.columns([1, 2])
    with col_kedi:
        avatar_goster("bekliyor", 350)
    with col_title:
        st.write("<br><br>", unsafe_allow_html=True)
        st.title("Cilt Tipinizi Belirleyelim 🌿")

    with st.form(key="quiz_form", border=False):
        st.markdown('<div class="question-card"><h3>1. Yüzünüzü yıkadıktan sonra cildiniz nasıl hisseder?</h3></div>',
                    unsafe_allow_html=True)
        s1 = st.radio("S1", ["Gergin ve kuruma eğilimli", "Rahat, normal", "T bölgesi yağlı, yanaklar kuru",
                             "Genel olarak parlak ve yağlı"], label_visibility="collapsed")

        st.markdown('<div class="question-card"><h3>2. Gözeneklerinizin görünümü nasıldır?</h3></div>',
                    unsafe_allow_html=True)
        s2 = st.radio("S2", ["Neredeyse hiç görünmez", "Sadece burun çevremde biraz belirgin", "Geniş ve belirgin"],
                      label_visibility="collapsed")

        st.markdown('<div class="question-card"><h3>3. Sivilce/siyah nokta problemi ne sıklıkla yaşarsınız?</h3></div>',
                    unsafe_allow_html=True)
        s3 = st.radio("S3", ["Çok nadir", "Dönemsel veya sadece T bölgesinde", "Sık sık, akneye eğilimli"],
                      label_visibility="collapsed")

        st.markdown('<div class="question-card"><h3>4. Cildiniz yeni ürünlere karşı hassas mıdır?</h3></div>',
                    unsafe_allow_html=True)
        s4 = st.radio("S4", ["Hayır, pek tepki vermez", "Bazen kızarır", "Evet, çok çabuk tahriş olur"],
                      label_visibility="collapsed")

        if st.form_submit_button("Analiz Panelini Aç ✨"):
            c_tipi = "Normal Cilt"
            if "Gergin" in s1:
                c_tipi = "Kuru Cilt"
            elif "T bölgesi" in s1:
                c_tipi = "Karma Cilt"
            elif "parlak ve yağlı" in s1:
                c_tipi = "Yağlı Cilt"
            if "tahriş olur" in s4: c_tipi += " ve Hassas"

            st.session_state.cilt_tipi = c_tipi
            st.session_state.test_bitti = True
            st.rerun()

# --- EKRAN 2: ANALİZ DASHBOARD ---
else:
    col_l, col_r = st.columns([1, 2], gap="large")

    with col_l:
        st.markdown(
            f"<div class='sonuc-karti'><h3>🐾 Profiliniz</h3><p>Cilt Tipi: <b>{st.session_state.cilt_tipi}</b></p></div>",
            unsafe_allow_html=True)
        avatar_goster(st.session_state.analiz_durumu, 300)

        if st.session_state.analiz_durumu == "analiz_ediyor":
            st.markdown("""
                <div class="loading-container">
                    <div class="loading-block"></div>
                    <div class="loading-text">İçerikler analiz ediliyor...</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)
        yuklenen_resim = st.file_uploader("Ürün fotoğrafını yükle", type=["jpg", "png", "jpeg"],
                                          label_visibility="collapsed")

        if yuklenen_resim is not None:
            if st.session_state.last_fn != yuklenen_resim.name:
                st.session_state.last_fn = yuklenen_resim.name
                st.session_state.analiz_durumu = "analiz_ediyor"
                st.session_state.kayitli_rapor = ""
                st.rerun()

        if st.button("🔄 Testi Baştan Çöz"):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()

    with col_r:
        if st.session_state.analiz_durumu == "analiz_ediyor" and yuklenen_resim:
            image = Image.open(yuklenen_resim)

            komut = f"""
            Sen profesyonel bir dermatoloji asistanısın. Markdown (**) KULLANMA. Sadece <b> ve <span> kullan.
            Kullanıcının cilt tipi: '{st.session_state.cilt_tipi}'.
            Aşağıdaki yapıyı koru:
            <div class='skor-kutusu'><p>Uyumluluk Skoru</p><p class='skor-deger'>%X</p></div>
            <div class="sonuc-karti"><h3>✅ Aktif İçerikler</h3>...</div>
            DİKKAT: Cevabının sonuna "DURUM:UYGUN" veya "DURUM:RISKLI" ekle.
            """

            cevap_kutusu = st.empty()
            tam_metin = ""

            try:
                # KRİTİK DEĞİŞİKLİK: gemini-1.5-flash-8b (Kota dostu model)
                response = client.models.generate_content_stream(model='gemini-2.5-flash-lite', contents=[image, komut])

                for chunk in response:
                    if chunk.text:
                        tam_metin += chunk.text
                        temiz_metin = tam_metin.replace("DURUM:UYGUN", "").replace("DURUM:RISKLI", "")
                        cevap_kutusu.markdown(temiz_metin, unsafe_allow_html=True)

                st.session_state.kayitli_rapor = tam_metin.replace("DURUM:UYGUN", "").replace("DURUM:RISKLI", "")
                st.session_state.analiz_durumu = "tamamlandi_uygun" if "DURUM:UYGUN" in tam_metin else "tamamlandi_uygun_degil"
                time.sleep(0.5)
                st.rerun()

            except Exception as e:
                st.error(f"Kota hatası oluştu, lütfen 30sn bekleyin. Hata: {e}")
                st.session_state.analiz_durumu = "bekliyor"

        elif st.session_state.kayitli_rapor:
            st.markdown(st.session_state.kayitli_rapor, unsafe_allow_html=True)