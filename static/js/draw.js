window.onload = function() {
  // Syncronize canvas size with server
  async function syncCanvasSize() {
    try {
      const resp = await fetch('/canvas/size');
      const { width, height } = await resp.json();
      canvas.width = width;
      canvas.height = height;
      clear();
    } catch (e) {
      console.log('Failed to sync canvas size:', e);
    }
  }

  // Refresh cache detection
  if (localStorage.getItem('sigCache')) {
    if (confirm('Unsaved changes detected, do you want to clear and sync the local canvas size?')) {
      localStorage.removeItem('sigCache');
      syncCanvasSize();
    } else {
      // Restore cached content
      const img = new Image();
      img.onload = function() {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };
      img.src = localStorage.getItem('sigCache');
    }
  } else {
    syncCanvasSize();
  }
  const canvas = document.getElementById('sigCanvas');
  const ctx = canvas.getContext('2d');
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  let drawing = false;

  function resizeCanvas() {
    // keep canvas logical size fixed; CSS can scale if needed
  }

  function clear() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0,0,canvas.width, canvas.height);
  }

  function getTouchPos(e) {
    const rect = canvas.getBoundingClientRect();
    const t = e.touches ? e.touches[0] : e;
    return { x: (t.clientX - rect.left) * (canvas.width/rect.width), y: (t.clientY - rect.top) * (canvas.height/rect.height) };
  }

  canvas.addEventListener('touchstart', e => { e.preventDefault(); drawing = true; const p = getTouchPos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); }, {passive:false});
  canvas.addEventListener('touchmove', e => { e.preventDefault(); if(!drawing) return; const p = getTouchPos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); }, {passive:false});
  canvas.addEventListener('touchend', e => { e.preventDefault(); drawing = false; }, {passive:false});

  // mouse fallback for desktop testing
  canvas.addEventListener('mousedown', e => { drawing = true; const p = getTouchPos(e); ctx.beginPath(); ctx.moveTo(p.x,p.y); });
  canvas.addEventListener('mousemove', e => { if(!drawing) return; const p = getTouchPos(e); ctx.lineTo(p.x,p.y); ctx.stroke(); });
  canvas.addEventListener('mouseup', e => { drawing = false; });

  document.getElementById('clearBtn').addEventListener('click', async function() {
    await syncCanvasSize();
    document.getElementById('status').textContent = 'Clean Canvas';
    console.log('[PhoneSign] Clean Canvas');
  });
  // Save drawing content to cache
  canvas.addEventListener('mouseup', e => {
    localStorage.setItem('sigCache', canvas.toDataURL('image/png'));
    drawing = false;
  });

  document.getElementById('doneBtn').addEventListener('click', async () => {
    // Directly upload the PNG file to the output folder
    const dataurl = canvas.toDataURL('image/png');
    document.getElementById('status').textContent = 'Uploading...';
    console.log('[PhoneSign] Push to PC...');
    try {
      // Convert dataurl to Blob
      const res = await fetch(dataurl);
      const blob = await res.blob();
      const formData = new FormData();
      // Name the file using time stamps
      const filename = 'signature_' + Date.now() + '.png';
      formData.append('photos', blob, filename);
      const resp = await fetch('/api/file_share/upload', {
        method: 'POST',
        body: formData
      });
      const j = await resp.json();
      if (j.success) {
        document.getElementById('status').textContent = 'Saved!';
        console.log('[PhoneSign] Signature saved to server (Saved!)');
      } else {
        document.getElementById('status').textContent = 'Error: ' + (j.error||'');
        console.log('[PhoneSign] Upload failed: ' + (j.error||''));
      }
    } catch (e) {
      document.getElementById('status').textContent = 'Upload failed';
      console.log('[PhoneSign] Upload error: ', e);
    }
  });

  // init
  clear();
  resizeCanvas();
  document.getElementById('status').textContent = 'Draw on this canvas';
};
