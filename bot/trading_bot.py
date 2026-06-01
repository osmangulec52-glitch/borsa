from binance.client import Client
from bot.strategies import EMA821Strategy
from bot.notifications import NotificationManager
from config import Config
import threading
import time
from datetime import datetime

class TradingBot:
    """Ana Trading Bot Sınıfı"""
    
    def __init__(self):
        self.config = Config
        self.client = Client(self.config.BINANCE_API_KEY, self.config.BINANCE_API_SECRET)
        self.strategy = EMA821Strategy(
            short_period=self.config.EMA_SHORT_PERIOD,
            long_period=self.config.EMA_LONG_PERIOD
        )
        self.notification_manager = NotificationManager()
        self.is_running = False
        self.tracked_symbols = {}
        self.thread = None
        self.last_signals = {}
    
    def get_klines(self, symbol, interval='1m', limit=100):
        """
        Binance'den mum verisini al
        
        Args:
            symbol: Kripto para sembolü (örn: BTCUSDT)
            interval: Zaman aralığı (1m, 5m, 15m, 1h, 1d)
            limit: Kaç mum
        
        Returns:
            list: Kapanış fiyatları
        """
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            prices = [float(kline[4]) for kline in klines]  # Kapanış fiyatları
            return prices
        except Exception as e:
            print(f"[Binance] Hata ({symbol}): {e}")
            return []
    
    def get_current_price(self, symbol):
        """
        Mevcut fiyatı al
        
        Args:
            symbol: Kripto para sembolü
        
        Returns:
            float: Mevcut fiyat
        """
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            print(f"[Binance] Hata ({symbol}): {e}")
            return None
    
    def analyze_symbol(self, symbol, interval='1m'):
        """
        Kripto para sembolünü analiz et
        
        Args:
            symbol: Kripto para sembolü
            interval: Zaman aralığı
        
        Returns:
            dict: Analiz sonuçları
        """
        prices = self.get_klines(symbol, interval, limit=100)
        current_price = self.get_current_price(symbol)
        
        if not prices or not current_price:
            return None
        
        analysis = self.strategy.analyze(prices)
        analysis['symbol'] = symbol
        analysis['price'] = current_price
        analysis['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        analysis['interval'] = interval
        
        return analysis
    
    def add_symbol(self, symbol, interval='1m'):
        """
        Takip edilecek sembol ekle
        
        Args:
            symbol: Kripto para sembolü
            interval: Zaman aralığı
        """
        if symbol not in self.tracked_symbols:
            self.tracked_symbols[symbol] = {
                'interval': interval,
                'last_signal': None,
                'last_analysis': None
            }
            print(f"[Bot] Sembol eklendi: {symbol}")
    
    def remove_symbol(self, symbol):
        """
        Takip edilmeden sembol kaldır
        
        Args:
            symbol: Kripto para sembolü
        """
        if symbol in self.tracked_symbols:
            del self.tracked_symbols[symbol]
            print(f"[Bot] Sembol kaldırıldı: {symbol}")
    
    def get_tracked_symbols(self):
        """Takip edilen semboller listesini getir"""
        return list(self.tracked_symbols.keys())
    
    def check_symbols(self):
        """Tüm semboller için kontrol yap"""
        for symbol in self.tracked_symbols.keys():
            analysis = self.analyze_symbol(
                symbol,
                self.tracked_symbols[symbol]['interval']
            )
            
            if not analysis:
                continue
            
            self.tracked_symbols[symbol]['last_analysis'] = analysis
            
            # Sinyal değişti mi kontrol et
            last_signal = self.tracked_symbols[symbol]['last_signal']
            current_signal = analysis['signal']
            
            if last_signal != current_signal or analysis['crossover']:
                self.tracked_symbols[symbol]['last_signal'] = current_signal
                
                # Bildirim gönder
                self._send_signal_notification(symbol, analysis)
    
    def _send_signal_notification(self, symbol, analysis):
        """Sinyal bildirimi gönder"""
        signal = analysis['signal']
        price = analysis['price']
        ema_short = analysis['ema_short']
        ema_long = analysis['ema_long']
        
        if signal == 'AL':
            title = f"🟢 AL SİNYALİ - {symbol}"
            message = f"EMA 8/21 kesişimi AL sinyali verdi!"
        elif signal == 'SAT':
            title = f"🔴 SAT SİNYALİ - {symbol}"
            message = f"EMA 8/21 kesişimi SAT sinyali verdi!"
        else:
            title = f"🟡 TUT SİNYALİ - {symbol}"
            message = f"Trend belirsiz, TUT önerisi."
        
        self.notification_manager.send_notification(
            title=title,
            message=message,
            signal=signal,
            symbol=symbol,
            price=price,
            ema_short=ema_short,
            ema_long=ema_long
        )
    
    def start(self):
        """Bot'u başlat"""
        if self.is_running:
            print("[Bot] Bot zaten çalışıyor.")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("[Bot] Bot başlatıldı.")
    
    def stop(self):
        """Bot'u durdur"""
        self.is_running = False
        print("[Bot] Bot durduruldu.")
    
    def _run(self):
        """Bot döngüsü"""
        print("[Bot] Döngü başladı.")
        while self.is_running:
            try:
                if self.tracked_symbols:
                    self.check_symbols()
                time.sleep(self.config.CHECK_INTERVAL)
            except Exception as e:
                print(f"[Bot] Hata: {e}")
                time.sleep(5)
    
    def get_analysis(self, symbol):
        """Son analizi getir"""
        if symbol in self.tracked_symbols:
            return self.tracked_symbols[symbol]['last_analysis']
        return None
    
    def get_all_analysis(self):
        """Tüm semboller için son analizi getir"""
        results = []
        for symbol in self.tracked_symbols.keys():
            analysis = self.tracked_symbols[symbol]['last_analysis']
            if analysis:
                results.append(analysis)
        return results
