const module = window.dootModule;

// State
let rawRows      = [];   // All parsed rows (arrays of strings)
let filteredRows = [];   // Rows after processing (including header)
let headerRowIdx = 0;    // 0-based index into rawRows
let colIdx       = 0;    // 0-based column index for identifier
let csvFilename  = 'processed.csv';
let processedCsv = ''; // Serialized CSV text after processing

// Event listeners

// Step 1: File selection
document.getElementById('doot-file-input').addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) { return; }
    csvFilename = file.name;

    const reader = new FileReader();
    reader.onload = ev => {
        rawRows = parseCsv(ev.target.result);
        renderHeaderPreview();
        document.getElementById('doot-preview-section').style.display = '';
    };
    reader.onerror = () => alert('Could not read the selected file.');
    reader.readAsText(file);
});

document.getElementById('doot-header-row').addEventListener('input', function () {
    const v = parseInt(this.value, 10);
    if (!isNaN(v) && v >= 1) {
        const clamped = Math.max(1, Math.min(v, rawRows.length));
        headerRowIdx = clamped - 1;
        renderHeaderPreview();
    }
});

document.getElementById('doot-step1-next').addEventListener('click', () => {
    if (rawRows.length === 0) {
        alert('Please select a CSV file first.');
        return;
    }
    headerRowIdx = parseInt(document.getElementById('doot-header-row').value, 10) - 1;
    if (isNaN(headerRowIdx) || headerRowIdx < 0 || headerRowIdx >= rawRows.length) {
        alert('Invalid header row selection.');
        return;
    }
    populateColumnDropdown();
    showStep(2);
});

// Step 2: Column selection
document.getElementById('doot-step2-back').addEventListener('click', () => {
    showStep(1);
});

document.getElementById('doot-step2-next').addEventListener('click', () => {
    colIdx = parseInt(document.getElementById('doot-id-column').value, 10);
    showStep(3);
});

// Step 3: Filter + Process
document.getElementById('doot-step3-back').addEventListener('click', () => {
    showStep(2);
});

document.getElementById('doot-process-btn').addEventListener('click', () => {
    const excludeText = document.getElementById('doot-exclude').value;
    const includeText = document.getElementById('doot-include').value;

    const excludeSet = buildSet(excludeText);
    const includeSet = buildSet(includeText);

    if (excludeSet.size === 0 && includeSet.size === 0) {
        if (!confirm('No filters entered — all data rows will be kept. Continue?')) return;
    }

    const dataRows = rawRows.slice(headerRowIdx + 1);

    let filtered = dataRows;

    if (excludeSet.size > 0) {
        filtered = filtered.filter(row => !excludeSet.has((row[colIdx] || '').trim()));
    }

    if (includeSet.size > 0) {
        filtered = filtered.filter(row => includeSet.has((row[colIdx] || '').trim()));
    }

    const removed   = dataRows.length - filtered.length;
    const remaining = filtered.length;

    // Prepend header row
    filteredRows = [rawRows[headerRowIdx]].concat(filtered);

    const msg = document.getElementById('doot-results-msg');
    msg.innerHTML =
        `<strong>${escapeHtml(removed)}</strong> row(s) removed. ` +
        `<strong>${escapeHtml(remaining)}</strong> row(s) remain.`;

    processedCsv = serialiseCsv(filteredRows);

    // Revoke any previous Blob URL to free memory
    const link = document.getElementById('doot-preview-link');
    if (link.dataset.blobUrl) {
        URL.revokeObjectURL(link.dataset.blobUrl);
    }

    const blob     = new Blob([processedCsv], { type: 'text/csv' });
    const blobUrl  = URL.createObjectURL(blob);
    const filename = `${csvFilename.replace(/\.csv$/i, '')}_processed.csv`;

    link.href            = blobUrl;
    link.download        = filename;
    link.dataset.blobUrl = blobUrl;

    showStep(4);
});

// Step 4: Upload
document.getElementById('doot-step4-back').addEventListener('click', () => {
    showStep(3);
});

document.getElementById('doot-upload-btn').addEventListener('click', () => {
    const b64      = encodeToBase64(processedCsv);
    const filename = `${csvFilename.replace(/\.csv$/i, '')}_processed.csv`;

    document.getElementById('doot-upload-progress').style.display = '';
    document.getElementById('doot-upload-btn').disabled = true;

    module.ajax('upload-file', { file_content: b64, filename: filename })
        .then(response => {
            document.getElementById('doot-upload-progress').style.display = 'none';
            document.getElementById('doot-upload-btn').disabled = false;

            if (response && response.success) {
                const doneMsg = document.getElementById('doot-done-msg');
                doneMsg.innerHTML =
                    `File uploaded successfully. ` +
                    `Record: <strong>${escapeHtml(response.record)}</strong>.`;
                showStep(5);
            } else {
                alert(`Upload failed: ${escapeHtml((response && response.error) || 'Unknown error')}`);
            }
        })
        .catch(err => {
            document.getElementById('doot-upload-progress').style.display = 'none';
            document.getElementById('doot-upload-btn').disabled = false;
            alert(`Upload error: ${escapeHtml(String(err))}`);
        });
});

// Step 5: Restart
document.getElementById('doot-restart-btn').addEventListener('click', () => {
    rawRows      = [];
    filteredRows = [];
    headerRowIdx = 0;
    colIdx       = 0;
    csvFilename  = 'processed.csv';
    processedCsv = '';

    const link = document.getElementById('doot-preview-link');
    if (link.dataset.blobUrl) {
        URL.revokeObjectURL(link.dataset.blobUrl);
        link.dataset.blobUrl = '';
        link.href = '#';
    }

    document.getElementById('doot-file-input').value              = '';
    document.getElementById('doot-preview-section').style.display = 'none';
    document.getElementById('doot-header-preview').innerHTML      = '';
    document.getElementById('doot-header-row').value              = '1';
    document.getElementById('doot-id-column').innerHTML           = '';
    document.getElementById('doot-exclude').value                 = '';
    document.getElementById('doot-include').value                 = '';

    showStep(1);
});

// Helper functions

/**
 * Shows the wizard step with the given number and hides all others.
 *
 * @param {number} n - Step number to display (1–5).
 */
function showStep(n) {
    [1, 2, 3, 4, 5].forEach(i => {
        document.getElementById(`doot-step-${i}`).classList.toggle('d-none', i !== n);
    });
}

/**
 * Renders a preview of the current header row into `#doot-header-preview`.
 */
function renderHeaderPreview() {
    const el = document.getElementById('doot-header-preview');
    const cells = (rawRows[headerRowIdx] || []).slice(0, 5);
    if (cells.length === 0) { el.textContent = ''; return; }
    const preview = cells.map(c => escapeHtml(c || '\u2013')).join(' &bull; ');
    const more = (rawRows[headerRowIdx] || []).length > 5
        ? ` &bull; <em>${(rawRows[headerRowIdx].length - 5)} more</em>` : '';
    el.innerHTML = 'Columns found: ' + preview + more;
}

/**
 * Populates the `#doot-id-column` `<select>` with one `<option>` per column
 * found in the current header row (`rawRows[headerRowIdx]`).
 */
function populateColumnDropdown() {
    const select  = document.getElementById('doot-id-column');
    const headers = rawRows[headerRowIdx] || [];
    select.innerHTML = '';
    headers.forEach((name, ci) => {
        const opt = document.createElement('option');
        opt.value = ci;
        opt.textContent = name || `Column ${ci + 1}`;
        select.appendChild(opt);
    });
}

/**
 * Parses a newline-delimited list of identifiers into a Set for lookup.
 *
 * @param {string} text - Newline-delimited identifier list (from a textarea).
 * @returns {Set<string>} Set of trimmed, non-empty identifier strings.
 */
function buildSet(text) {
    const s = new Set();
    text.split('\n').forEach(line => {
        const t = line.trim();
        if (t !== '') { s.add(t); }
    });
    return s;
}

/**
 * Encodes a UTF-8 string to a Base64 string ready for upload.
 *
 * @param {string} str - The UTF-8 string to encode.
 * @returns {string} Base64-encoded representation of `str`.
 */
function encodeToBase64(str) {
    const bytes = new TextEncoder().encode(str);
    let binary  = '';
    const chunk = 8192;
    for (let offset = 0; offset < bytes.length; offset += chunk) {
        binary += String.fromCharCode(...bytes.subarray(offset, offset + chunk));
    }
    return btoa(binary);
}

/**
 * Escapes a value for safe insertion into HTML content.
 *
 * @param {*} s - The value to escape.
 * @returns {string} HTML-safe string.
 */
function escapeHtml(s) {
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/**
 * Parses a CSV string into a two-dimensional array of field values.
 *
 * @param {string} text - Raw CSV text to parse.
 * @returns {string[][]} Array of rows, each row being an array of field strings.
 */
function parseCsv(text) {
    let rows   = [];
    let row    = [];
    let field  = '';
    let quoted = false;
    let i      = 0;
    let len    = text.length;

    while (i < len) {
        let ch = text[i];

        if (quoted) {
            if (ch === '"') {
                if (i + 1 < len && text[i + 1] === '"') {
                    // Escaped quote
                    field += '"';
                    i += 2;
                } else {
                    // End of quoted field
                    quoted = false;
                    i++;
                }
            } else {
                field += ch;
                i++;
            }
        } else {
            if (ch === '"') {
                quoted = true;
                i++;
            } else if (ch === ',') {
                row.push(field);
                field = '';
                i++;
            } else if (ch === '\r') {
                row.push(field);
                field = '';
                rows.push(row);
                row = [];
                i++;
                if (i < len && text[i] === '\n') {
                    i++;
                }
            } else if (ch === '\n') {
                row.push(field);
                field = '';
                rows.push(row);
                row = [];
                i++;
            } else {
                field += ch;
                i++;
            }
        }
    }

    // Push last field/row if non-empty
    if (field !== '' || row.length > 0) {
        row.push(field);
        rows.push(row);
    }

    // Drop trailing empty row that can appear from a trailing newline
    if (rows.length > 0) {
        const last = rows[rows.length - 1];
        if (last.length === 1 && last[0] === '') {
            rows.pop();
        }
    }

    return rows;
}

/**
 * Serializes a two-dimensional array of field values to a CSV string.
 *
 * @param {string[][]} rows - Array of rows, each an array of field strings.
 * @returns {string} CSV text with CRLF line endings.
 */
function serialiseCsv(rows) {
    return rows.map(row =>
        row.map(field => {
            if (field.includes(',') ||
                field.includes('"') ||
                field.includes('\n') ||
                field.includes('\r')) {
                return `"${field.replace(/"/g, '""')}"`;
            }
            return field;
        }).join(',')
    ).join('\r\n');
}