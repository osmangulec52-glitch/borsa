import requests
from datetime import datetime
from config import Config

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

class NotificationManager:
    """Bildirim Yöneticisi"""
    
    def __init__(self):
        self.config = Config
        self.history = []
    
    def send_notification(self, title, message, signal=None, symbol=None, price=None, ema_short=None, ema_long=None):
        """
        Tüm kanallara bildirim gönder
        
        Args:
            title: Başlık
            message: İçerik
            signal: AL/SAT/TUT
            symbol: Kripto para sembolü
            price: Mevcut fiyat
            ema_short: EMA 8 değeri
            ema_long: EMA 21 değeri
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        notification_data = {
            'timestamp': timestamp,
            'title': title,
            'message': message,
            'signal': signal,
            'symbol': symbol,
            'price': price,
            'ema_short': ema_short,
            'ema_long': ema_long
        }
        
        self.history.append(notification_data)
        
        # Discord'a gönder
        if self.config.DISCORD_ENABLED:
            self._send_discord(title, message, signal, symbol, price, ema_short, ema_long, timestamp)
        
        # Telegram'a gönder
        if self.config.TELEGRAM_ENABLED:
            self._send_telegram(title, message, signal, symbol, price, ema_short, ema_long, timestamp)
        
        # Desktop bildirimi
        if self.config.DESKTOP_NOTIFICATIONS_ENABLED:
            self._send_desktop(title, message)
    
    def _send_discord(self, title, message, signal, symbol, price, ema_short, ema_long, timestamp):
        """Discord webhook'a gönder"""
        if not self.config.DISCORD_WEBHOOK_URL:
            return
        
        try:
            # Sinyal rengini belirle
            if signal == 'AL':
                color = 0x00FF00  # Yeşil
            elif signal == 'SAT':
                color = 0xFF0000  # Kırmızı
            else:
                color = 0xFFFF00  # Sarı
            
            embed = {
                "embeds": [{
                    "title": f"🤖 {title}",
                    "description": message,
                    "color": color,
                    "fields": [
                        {"name": "Signal", "value": signal or "N/A", "inline": True},
                        {"name": "Symbol", "value": symbol or "N/A", "inline": True},
                        {"name": "Price", "value": f"${price}" if price else "N/A", "inline": True},
                        {"name": "EMA 8", "value": str(ema_short) if ema_short else "N/A", "inline": True},
                        {"name": "EMA 21", "value": str(ema_long) if ema_long else "N/A", "inline": True},
                    ],
                    "timestamp": timestamp
                }]
            }
            
            response = requests.post(self.config.DISCORD_WEBHOOK_URL, json=embed, timeout=5)
            response.raise_for_status()
            print(f"[Discord] Bildirim gönderildi: {title}")
        except Exception as e:
            print(f"[Discord] Hata: {e}")
    
    def _send_telegram(self, title, message, signal, symbol, price, ema_short, ema_long, timestamp):
        """Telegram'a gönder"""
        if not self.config.TELEGRAM_BOT_TOKEN or not self.config.TELEGRAM_CHAT_ID:
            return
        
        try:
            # Sinyal emoji
            emoji = "🟢" if signal == "AL" else "🔴" if signal == "SAT" else "🟡"
            
            telegram_message = f"""
{emoji} **{title}**

{message}

**Signal:** {signal or 'N/A'}
**Symbol:** {symbol or 'N/A'}
**Price:** ${price if price else 'N/A'}
**EMA 8:** {ema_short if ema_short else 'N/A'}
**EMA 21:** {ema_long if ema_long else 'N/A'}
**Time:** {timestamp}
            """
            
            url = f"https://api.telegram.org/bot{self.config.TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": self.config.TELEGRAM_CHAT_ID,
                "text": telegram_message,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, data=data, timeout=5)
            response.raise_for_status()
            print(f"[Telegram] Bildirim gönderildi: {title}")
        except Exception as e:
            print(f"[Telegram] Hata: {e}")
    
    def _send_desktop(self, title, message):
        """Desktop bildirimi gönder"""
        if not PLYER_AVAILABLE:
            return
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Crypto Trading Bot",
                timeout=10
            )
            print(f"[Desktop] Bildirim gösterildi: {title}")
        except Exception as e:
            print(f"[Desktop] Hata: {e}")
    
    def get_history(self):
        """Bildirim geçmişini getir"""
        return self.history[-50:]  # Son 50 bildirimi döndür
