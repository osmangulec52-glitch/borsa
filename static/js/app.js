// DOM Elements
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const testBtn = document.getElementById('testBtn');
const addBtn = document.getElementById('addBtn');
const symbolInput = document.getElementById('symbolInput');
const intervalSelect = document.getElementById('intervalSelect');
const statusText = document.getElementById('statusText');
const analysisContainer = document.getElementById('analysisContainer');
const notificationsContainer = document.getElementById('notificationsContainer');

// Event Listeners
startBtn.addEventListener('click', startBot);
stopBtn.addEventListener('click', stopBot);
testBtn.addEventListener('click', testNotification);
addBtn.addEventListener('click', addSymbol);
symbolInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addSymbol();
});

// Initialize
window.addEventListener('load', () => {
    updateStatus();
    setInterval(updateStatus, 5000);
    setInterval(updateAnalysis, 5000);
    setInterval(updateNotifications, 5000);
});

// API Functions
async function startBot() {
    try {
        const response = await fetch('/api/start', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            showAlert('Bot başlatıldı!', 'success');
            updateStatus();
        }
    } catch (error) {
        showAlert('Hata: ' + error.message, 'error');
    }
}

async function stopBot() {
    try {
        const response = await fetch('/api/stop', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            showAlert('Bot durduruldu!', 'success');
            updateStatus();
        }
    } catch (error) {
        showAlert('Hata: ' + error.message, 'error');
    }
}

async function testNotification() {
    try {
        const response = await fetch('/api/test-notification', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            showAlert('Test bildirimi gönderildi!', 'success');
        }
    } catch (error) {
        showAlert('Hata: ' + error.message, 'error');
    }
}

async function addSymbol() {
    const symbol = symbolInput.value.trim().toUpperCase();
    const interval = intervalSelect.value;
    
    if (!symbol) {
        showAlert('Lütfen bir sembol girin!', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/add-symbol', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, interval })
        });
        const data = await response.json();
        if (data.success) {
            showAlert(`${symbol} eklendi!`, 'success');
            symbolInput.value = '';
            updateAnalysis();
        } else {
            showAlert('Hata: ' + data.message, 'error');
        }
    } catch (error) {
        showAlert('Hata: ' + error.message, 'error');
    }
}

async function removeSymbol(symbol) {
    if (!confirm(`${symbol} silinsin mi?`)) return;
    
    try {
        const response = await fetch(`/api/remove-symbol/${symbol}`, { method: 'DELETE' });
        const data = await response.json();
        if (data.success) {
            showAlert(`${symbol} kaldırıldı!`, 'success');
            updateAnalysis();
        }
    } catch (error) {
        showAlert('Hata: ' + error.message, 'error');
    }
}

async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const isRunning = data.running;
        statusText.textContent = isRunning ? 'Çalışıyor' : 'Durduruldu';
        statusText.className = isRunning ? 'running' : '';
        
        startBtn.disabled = isRunning;
        stopBtn.disabled = !isRunning;
    } catch (error) {
        console.error('Status error:', error);
    }
}

async function updateAnalysis() {
    try {
        const response = await fetch('/api/analysis');
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            analysisContainer.innerHTML = data.data.map(analysis => 
                createAnalysisCard(analysis)
            ).join('');
            
            // Add event listeners to remove buttons
            document.querySelectorAll('.remove-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    removeSymbol(e.target.dataset.symbol);
                });
            });
        } else {
            analysisContainer.innerHTML = '<p class="no-data">Henüz sembol eklenmedi...</p>';
        }
    } catch (error) {
        console.error('Analysis error:', error);
    }
}

async function updateNotifications() {
    try {
        const response = await fetch('/api/notifications');
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            notificationsContainer.innerHTML = data.data.map(notif => 
                createNotificationItem(notif)
            ).join('');
        } else {
            notificationsContainer.innerHTML = '<p class="no-data">Henüz bildirim yok...</p>';
        }
    } catch (error) {
        console.error('Notifications error:', error);
    }
}

// UI Functions
function createAnalysisCard(analysis) {
    const signal = analysis.signal || 'TUT';
    const signalClass = signal === 'AL' ? 'al' : signal === 'SAT' ? 'sat' : 'tut';
    const signalEmoji = signal === 'AL' ? '🟢' : signal === 'SAT' ? '🔴' : '🟡';
    
    return `
        <div class="analysis-card signal-${signalClass}">
            <button class="remove-btn" data-symbol="${analysis.symbol}">×</button>
            <div class="card-header">
                <span class="symbol-name">${analysis.symbol}</span>
                <span class="signal-badge ${signalClass}">${signalEmoji} ${signal}</span>
            </div>
            <div class="card-content">
                <div class="info-row">
                    <span class="info-label">Fiyat:</span>
                    <span class="info-value">$${analysis.price?.toFixed(2) || 'N/A'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">EMA 8:</span>
                    <span class="info-value">${analysis.ema_short?.toFixed(2) || 'N/A'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">EMA 21:</span>
                    <span class="info-value">${analysis.ema_long?.toFixed(2) || 'N/A'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Güvenilirlik:</span>
                    <span class="info-value">${analysis.confidence?.toFixed(1) || 'N/A'}%</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Zaman:</span>
                    <span class="info-value" style="font-size: 0.9em;">${analysis.timestamp || 'N/A'}</span>
                </div>
            </div>
        </div>
    `;
}

function createNotificationItem(notif) {
    const signalClass = notif.signal === 'AL' ? 'al' : notif.signal === 'SAT' ? 'sat' : 'tut';
    
    return `
        <div class="notification-item ${signalClass}">
            <div class="notification-title">${notif.title}</div>
            <div class="notification-details">
                <strong>${notif.symbol || 'N/A'}</strong> - ${notif.message || ''}
            </div>
            <div class="notification-time">${notif.timestamp || 'N/A'}</div>
        </div>
    `;
}

function showAlert(message, type) {
    // Simple alert - you can replace with a better notification system
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Visual feedback
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => alert.remove(), 3000);
}
