document.addEventListener('DOMContentLoaded', function() {
    const apiBase = '/api/file_share';

    function fetchFiles() {
        fetch(apiBase + '/files')
            .then(res => res.json())
            .then(data => renderFiles(data))
            .catch(() => alert('Can not obtain file list'));
    }

    function renderFiles(files) {
        const fileList = document.getElementById('file-list');
        fileList.innerHTML = '<label>Select Files to save：</label>';
        const table = document.createElement('table');
        table.className = 'table table-bordered';
        const thead = document.createElement('thead');
        thead.innerHTML = '<table><tr><th></th><th>File Name</th><th>Extension</th><th>Size</th><th>Date</th></tr></table>';
        table.appendChild(thead);
        const tbody = document.createElement('tbody');
        files.forEach(file => {
            const tr = document.createElement('tr');
            // Checkbox cell
            const tdCheck = document.createElement('td');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = file.name + file.ext;
            checkbox.className = 'form-check-input';
            tdCheck.appendChild(checkbox);
            tr.appendChild(tdCheck);
            // Other info cell
            const tdName = document.createElement('td');
            tdName.textContent = file.name;
            tr.appendChild(tdName);
            const tdExt = document.createElement('td');
            tdExt.textContent = file.ext;
            tr.appendChild(tdExt);
            const tdSize = document.createElement('td');
            tdSize.textContent = file.size;
            tr.appendChild(tdSize);
            const tdDate = document.createElement('td');
            tdDate.textContent = new Date(file.mtime * 1000).toLocaleString();
            tr.appendChild(tdDate);
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        fileList.appendChild(table);
        document.getElementById('download-selected').disabled = files.length === 0;
    }

    function getSelectedFiles() {
        return Array.from(document.querySelectorAll('#file-list input[type=checkbox]:checked'))
                    .map(cb => cb.value);
    }

    document.getElementById('download-selected').addEventListener('click', function() {
        const files = getSelectedFiles();
        if (!files.length) {
            alert('Please select files to download');
            return;
        }
        files.forEach(file => {
            const url = apiBase + '/download?filename=' + encodeURIComponent(file);
            const a = document.createElement('a');
            a.href = url;
            a.download = file;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
    });

    fetchFiles();
});