document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('textInput');
    const clearBtn = document.getElementById('clearBtn');
    const pasteBtn = document.getElementById('pasteBtn');
    const pushBtn = document.getElementById('pushBtn');
    const copyBtn = document.getElementById('copyBtn');
    const openBtn = document.getElementById('openBtn');
    const controlbar = document.getElementById('controlbar');
    const statusSpan = document.getElementById('status');

    function showStatus(msg) {
        statusSpan.textContent = msg;
    }

    function updateControlbar() {
        const val = textInput.value.trim();
        if (val) {
            controlbar.style.display = 'block';
            pushBtn.disabled = false;
            pushBtn.dataset.qr = val;
            copyBtn.disabled = false;
            copyBtn.style.color = 'black';
            copyBtn.dataset.qr = val;
            let urlPattern = /^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/\S*)?$/;
            if (urlPattern.test(val)) {
                openBtn.disabled = false;
                openBtn.style.color = 'black';
                openBtn.dataset.qr = val;
            } else {
                openBtn.disabled = true;
                openBtn.style.color = 'gray';
                openBtn.dataset.qr = '';
            }
        } else {
            controlbar.style.display = 'none';
            pushBtn.disabled = true;
            copyBtn.disabled = true;
            openBtn.disabled = true;
        }
    }

    clearBtn.addEventListener('click', function() {
        textInput.value = '';
        textInput.focus();
        updateControlbar();
    });

    pasteBtn.addEventListener('click', async function() {
        if (navigator.clipboard && window.isSecureContext) {
            try {
                const clipText = await navigator.clipboard.readText();
                const start = textInput.selectionStart;
                const end = textInput.selectionEnd;
                const before = textInput.value.substring(0, start);
                const after = textInput.value.substring(end);
                textInput.value = before + clipText + after;
                const cursor = start + clipText.length;
                textInput.selectionStart = textInput.selectionEnd = cursor;
                textInput.focus();
                updateControlbar();
            } catch (err) {
                alert('Failed to read clipboard: ' + err);
            }
        } else {
            alert('Clipboard API not supported or not in secure context.');
        }
    });

    textInput.addEventListener('input', updateControlbar);

    copyBtn.onclick = function() {
        let val = copyBtn.dataset.qr;
        if (!val) return;
        navigator.clipboard.writeText(val).then(() => {
            showStatus('Copied to clipboard');
        }, () => {
            showStatus('Copy failed');
        });
    };

    openBtn.onclick = function() {
        let val = openBtn.dataset.qr;
        if (!val) return;
        let url = val.match(/^https?:\/\//) ? val : ('https://' + val);
        window.open(url, '_blank');
    };

    pushBtn.onclick = function() {
        let val = pushBtn.dataset.qr;
        if (!val) return;
        showStatus('Uploading...');
        const formData = new FormData();
        const filename = 'text_' + Date.now() + '.txt';
        const blob = new Blob([val], { type: 'text/plain' });
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

    // 初始化
    updateControlbar();
    showStatus('Ready');
});
