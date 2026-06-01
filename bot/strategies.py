import pandas as pd
import numpy as np

class EMA821Strategy:
    """EMA 8/21 Kesişim Stratejisi"""
    
    def __init__(self, short_period=8, long_period=21):
        self.short_period = short_period
        self.long_period = long_period
    
    def calculate_ema(self, prices, period):
        """EMA hesapla"""
        return pd.Series(prices).ewm(span=period, adjust=False).mean()
    
    def analyze(self, prices):
        """
        Fiyat verisi ile analiz yap
        
        Args:
            prices: Fiyat listesi
        
        Returns:
            dict: {
                'signal': 'AL' | 'SAT' | 'TUT',
                'ema_short': float,
                'ema_long': float,
                'crossover': boolean,
                'confidence': float
            }
        """
        if len(prices) < self.long_period:
            return {
                'signal': 'TUT',
                'ema_short': None,
                'ema_long': None,
                'crossover': False,
                'confidence': 0.0,
                'message': 'Yetersiz veri'
            }
        
        prices_array = np.array(prices)
        ema_short = self.calculate_ema(prices_array, self.short_period)
        ema_long = self.calculate_ema(prices_array, self.long_period)
        
        # Son 2 değeri kontrol et
        ema_short_last = ema_short.iloc[-1]
        ema_long_last = ema_long.iloc[-1]
        ema_short_prev = ema_short.iloc[-2]
        ema_long_prev = ema_long.iloc[-2]
        
        # Kesişim kontrolü
        crossover = (ema_short_prev <= ema_long_prev and ema_short_last > ema_long_last) or \
                   (ema_short_prev >= ema_long_prev and ema_short_last < ema_long_last)
        
        # Sinyal belirle
        if ema_short_last > ema_long_last:
            signal = 'AL'
        elif ema_short_last < ema_long_last:
            signal = 'SAT'
        else:
            signal = 'TUT'
        
        # Güvenilirlik (kesişim ne kadar yakın)
        diff_percent = abs(ema_short_last - ema_long_last) / ema_long_last * 100
        confidence = min(100, max(0, 100 - diff_percent * 10))  # 0-100
        
        return {
            'signal': signal,
            'ema_short': round(float(ema_short_last), 2),
            'ema_long': round(float(ema_long_last), 2),
            'crossover': crossover,
            'confidence': round(float(confidence), 2),
            'message': f"EMA8: {ema_short_last:.2f}, EMA21: {ema_long_last:.2f}"
        }
