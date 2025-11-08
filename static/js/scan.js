let resultDiv = document.getElementById('qrResult');
let copyBtn = document.getElementById('copyBtn');
let openBtn = document.getElementById('openBtn');
let pushBtn = document.getElementById('pushBtn');
let statusSpan = document.getElementById('status');
let scanning = false;
let lastQr = null;
let qrReader = null;
let startBtn = document.getElementById('startBtn');

function showStatus(msg) {
  statusSpan.textContent = msg;
}

function startScan() {
  if (scanning) {
    // Scanning in progress, click to stop
    if (qrReader) {
      qrReader.stop().then(() => {
        scanning = false;
        showStatus('Click "Start Scan" to begin');
        startBtn.textContent = 'Start Scan';
        resultDiv.textContent = '';
        pushBtn.disabled = true;
        copyBtn.disabled = true;
        openBtn.disabled = true;
        copyBtn.style.color = 'gray';
        openBtn.style.color = 'gray';
      });
    }
    return;
  }
  scanning = true;
  showStatus('Starting camera...');
  qrReader = new Html5Qrcode("qr-reader");
  qrReader.start(
    { facingMode: "environment" },
    {
      fps: 10,
      qrbox: 250
    },
    qrCodeMessage => {
      showStatus('QR Detected!');
      resultDiv.textContent = 'Contents:' + qrCodeMessage;
        // Scanning successful, show button area
        document.getElementById('controlbar').style.display = 'block';
      pushBtn.disabled = false;
      pushBtn.dataset.qr = qrCodeMessage;
      copyBtn.disabled = false;
      copyBtn.style.color = 'black';
      copyBtn.dataset.qr = qrCodeMessage;
      let urlPattern = /^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/\S*)?$/;
      if (urlPattern.test(qrCodeMessage)) {
        openBtn.disabled = false;
        openBtn.style.color = 'black';
        openBtn.dataset.qr = qrCodeMessage;
      } else {
        openBtn.disabled = true;
        openBtn.style.color = 'gray';
        openBtn.dataset.qr = '';
      }
      lastQr = qrCodeMessage;
      qrReader.stop();
      scanning = false;
      startBtn.textContent = 'Start Scan';
      console.log('QR code captured and decoded successfully:', qrCodeMessage);
    },
    errorMessage => {
      // Optional: Show error message
      // showStatus('Scanning...');
    }
  ).then(() => {
    // Camera started successfully
    showStatus('Ready to Scan');
    startBtn.textContent = 'Stop Scan';
  }).catch(err => {
    showStatus('Camera error: ' + err);
    resultDiv.textContent = 'Cannot access camera: ' + err;
    scanning = false;
    startBtn.textContent = 'Start Scan';
  });
}

startBtn.onclick = startScan;

copyBtn.onclick = function() {
  let qr = copyBtn.dataset.qr;
  if (!qr) return;
  navigator.clipboard.writeText(qr).then(() => {
    showStatus('Copied to clipboard');
  }, () => {
    showStatus('Copy failed');
  });
};

openBtn.onclick = function() {
  let qr = openBtn.dataset.qr;
  if (!qr) return;
  let url = qr.match(/^https?:\/\//) ? qr : ('https://' + qr);
  window.open(url, '_blank');
};

pushBtn.onclick = function() {
  let qr = pushBtn.dataset.qr;
  if (!qr) return;
  showStatus('Uploading...');
  // Directly save the string as a text file and upload it to the output folder
  const formData = new FormData();
  // Name the file using time stamps
  const filename = 'scan_' + Date.now() + '.txt';
  const blob = new Blob([qr], { type: 'text/plain' });
  formData.append('photos', blob, filename);
  fetch('/api/file_share/upload', {
    method: 'POST',
    body: formData
  }).then(resp => resp.json()).then(j => {
    if (j.success) {
      showStatus('Saved!');
    } else {
      showStatus('Upload error: ' + (j.error||''));
    }
  }).catch(e => {
    showStatus('Upload failed');
  });
};

// Page load status
showStatus('Click "Start Scan" to begin');
