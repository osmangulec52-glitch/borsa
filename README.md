# Kripto Trading Bot - EMA 8/21 Strateji

Binance API'den gerçek zamanlı kripto para verisi çeken, EMA 8/21 kesişimine dayalı al/sat önerileri sunan ve Discord/Telegram/Desktop bildirimleri gönderen web tabanlı trading bot.

## Özellikler

✅ Binance API'den gerçek zamanlı veri
✅ EMA 8/21 kesişim stratejisi
✅ Discord webhook bildirimleri
✅ Telegram bot bildirimleri
✅ Desktop bildirimleri
✅ Web tabanlı dashboard
✅ Kullanıcı tarafından kripto para seçimi
✅ İşlem geçmişi ve istatistikler

## Kurulum

### 1. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. .env Dosyası Oluşturun

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin ve aşağıdaki bilgileri ekleyin:

```
# Binance API
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

# Discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Flask
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key_here
```

## Çalıştırma

```bash
python app.py
```

Tarayıcıda `http://localhost:5000` adresine gidin.

## API Bilgilerini Nasıl Alacağınız

### Discord Webhook URL
1. Discord sunucunuza gidin
2. Bir kanal seçin → Kanal Ayarları → Webhooks
3. "Yeni Webhook" oluşturun
4. URL'yi kopyalayın

### Telegram Bot Token
1. Telegram'da `@BotFather` ile sohbet açın
2. `/newbot` yazın
3. Bot adı ve kullanıcı adı girin
4. Token'ı kopyalayın
5. `/getid` yazarak chat ID'nizi alın

### Binance API
1. Binance.com'a gidin
2. API Management bölümüne gidin
3. Yeni API key oluşturun
4. API Key ve Secret Key'i kopyalayın

## Dosya Yapısı

```
.
├── app.py                 # Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── .env.example          # Ortam değişkenleri örneği
├── config.py             # Konfigürasyon
├── bot/
│   ├── __init__.py
│   ├── trading_bot.py    # Ana trading bot sınıfı
│   ├── strategies.py     # EMA 8/21 stratejisi
│   └── notifications.py  # Discord/Telegram/Desktop bildirimleri
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chart.js
└── templates/
    └── index.html        # Web dashboard
```

## Stratejisi

- **EMA 8**: 8 periyotlu Exponential Moving Average
- **EMA 21**: 21 periyotlu Exponential Moving Average
- **AL Sinyali**: EMA 8 > EMA 21 (kesişim yukarıya)
- **SAT Sinyali**: EMA 8 < EMA 21 (kesişim aşağıya)
- **TUT Sinyali**: Trend belirsiz

## Lisans

MIT
