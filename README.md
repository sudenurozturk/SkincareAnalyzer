# 🐾 Skincare Analyzer (Cilt Bakım Analizörü)

Bu proje, kullanıcıların cilt tiplerini belirlemelerine ve cilt bakım ürünlerinin içeriklerini yapay zeka desteğiyle analiz etmelerine yardımcı olan bir web uygulamasıdır. **Google Gemini 2.5 Flash Lite** teknolojisi kullanılarak geliştirilmiştir.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)

## 🌟 Özellikler

- **Akıllı Cilt Anketi:** Kullanıcının verdiği yanıtlara göre cilt tipini (Kuru, Yağlı, Karma, Hassas) anında belirler.
- **Yapay Zeka Destekli Analiz:** Ürün içerik listesinin fotoğrafını yükleyerek içeriklerin cildinizle uyumunu öğrenebilirsiniz.
- **Uyumluluk Skoru:** Ürünün kullanıcı cilt tipine uygunluğunu % üzerinden değerlendirir.
- **Kritik Uyarılar:** Alkol, parfüm ve diğer potansiyel tahriş edici maddeleri tespit ederek kullanıcıyı uyarır.
- **Kullanıcı Dostu Arayüz:** Modern, pastel tonlarda ve interaktif bir tasarım.

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için:

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/sudenurozturk/Skincare-Analyzer.git](https://github.com/sudenurozturk/Skincare-Analyzer.git)

   Gerekli kütüphaneleri yükleyin:

2. Gerekli kütüphaneleri yükleyin:
pip install -r requirements.txt

3.Ana dizine bir .env dosyası oluşturun ve Gemini API anahtarınızı ekleyin:
GOOGLE_API_KEY=your_api_key_here

4. Uygulamayı başlatın:
streamlit run main.py


Teknik Detaylar
Frontend/Backend: Streamlit (Python tabanlı)

Yapay Zeka: Google Gemini 2.5 Flash Lite (Vision Capabilities)

Görsel İşleme: PIL (Pillow)

Güvenlik: API anahtarları .env ve .gitignore ile korunmaktadır.

⚠️ Yasal Uyarı
Bu uygulama bilgilendirme amaçlıdır ve tıbbi tavsiye niteliği taşımaz. Herhangi bir ürünü kullanmadan önce mutlaka bir dermatoloğa danışınız.

Geliştiren: Sude Nur Öztürk
