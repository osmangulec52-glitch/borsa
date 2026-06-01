from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from bot import TradingBot
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Global bot instance
bot = TradingBot()
bot_started = False

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Bot'u başlat"""
    global bot_started
    try:
        if not bot_started:
            bot.start()
            bot_started = True
        return jsonify({'success': True, 'message': 'Bot başlatıldı'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Bot'u durdur"""
    global bot_started
    try:
        if bot_started:
            bot.stop()
            bot_started = False
        return jsonify({'success': True, 'message': 'Bot durduruldu'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/status')
def get_status():
    """Bot durumunu getir"""
    return jsonify({
        'running': bot.is_running,
        'tracked_symbols': bot.get_tracked_symbols(),
        'check_interval': app.config['CHECK_INTERVAL']
    })

@app.route('/api/add-symbol', methods=['POST'])
def add_symbol():
    """Sembol ekle"""
    try:
        data = request.json
        symbol = data.get('symbol', '').upper()
        interval = data.get('interval', '1m')
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Sembol gerekli'}), 400
        
        bot.add_symbol(symbol, interval)
        return jsonify({'success': True, 'message': f'{symbol} eklendi'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/remove-symbol/<symbol>', methods=['DELETE'])
def remove_symbol(symbol):
    """Sembol kaldır"""
    try:
        bot.remove_symbol(symbol.upper())
        return jsonify({'success': True, 'message': f'{symbol} kaldırıldı'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analysis')
def get_analysis():
    """Tüm semboller için analiz getir"""
    try:
        analysis = bot.get_all_analysis()
        return jsonify({
            'success': True,
            'data': analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analysis/<symbol>')
def get_symbol_analysis(symbol):
    """Belirli bir sembol için analiz getir"""
    try:
        analysis = bot.get_analysis(symbol.upper())
        if analysis:
            return jsonify({'success': True, 'data': analysis})
        else:
            return jsonify({'success': False, 'message': 'Sembol bulunamadı'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notifications')
def get_notifications():
    """Bildirimleri getir"""
    try:
        notifications = bot.notification_manager.get_history()
        return jsonify({'success': True, 'data': notifications})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/test-notification', methods=['POST'])
def test_notification():
    """Test bildirimi gönder"""
    try:
        bot.notification_manager.send_notification(
            title="🤖 Test Bildirimi",
            message="Bu bir test bildirimidir.",
            signal="AL",
            symbol="BTCUSDT",
            price=50000.00,
            ema_short=49900.00,
            ema_long=49800.00
        )
        return jsonify({'success': True, 'message': 'Test bildirimi gönderildi'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
