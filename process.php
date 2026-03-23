<?php

use Nottingham\DataOptOutTool\DataOptOutTool;

/** @var DataOptOutTool $module */
$module->initializeJavascriptModuleObject();
$jsModuleName = $module->getJavascriptModuleObjectName();

$instructionText = $module->escape( $module->getProjectSetting('instruction-text') );
$instructionText = preg_replace( '!&lt;(?:(?<t1>a)( href=&quot;(?(?=&quot;)|.)*&quot;)' .
                                 '(?: target=&quot;_blank&quot;)?|(?<t2>b|i))&gt;((?(?=&lt;/' .
                                 '(?:(?P=t1)|(?P=t2))&gt;)|.)*)&lt;/((?P=t1)|(?P=t2))&gt;!',
                                 '<$5$2>$4</$5>', $instructionText );
$instructionText = str_replace( [ '<a href=&quot;', '&quot;>' ],
                                [ '<a href="', '" target="_blank">' ], $instructionText );
$instructionText = nl2br( $instructionText, false );
$instructionIcon = 'fa-circle-info';
$instructionStyle = 'background: #c2e0f4; border: solid 2px #236fa1';
if ( $module->getProjectSetting('instruction-style') == 'warn' )
{
	$instructionIcon = 'fa-triangle-exclamation';
	$instructionStyle = 'background: #fbeeb8; border: solid 2px #d6a400';
}
$instructionStyle .= '; border-radius: 5px; margin: 25px 0; padding: 7px; display: flex; gap: 5px;';
?>
<h3 style="margin-bottom:20px">Process Opt-Outs</h3>

<!-- Step 1: File selection + header row -->
<div id="doot-step-1">
<?php
    if ( $instructionText != '' )
    {
?>
    <div style="<?php echo $instructionStyle; ?>">
        <i class="fas <?php echo $instructionIcon; ?> fs20"></i>
        <div>
            <?php echo $instructionText, "\n"; ?>
        </div>
    </div>
<?php
    }
?>
    <div class="mb-3">
        <label for="doot-file-input" class="form-label fw-bold">Select CSV file</label>
        <input type="file" id="doot-file-input" class="form-control" accept=".csv,text/csv">
    </div>
    <p class="text-muted small" style="margin-bottom:15px">
        <i class="fas fa-lock me-1"></i>
        Processing happens entirely on your device — no data is sent to REDCap until you
        click <strong>Upload</strong> in the final step, after filtering is applied.
    </p>
    <div id="doot-preview-section" style="display:none;">
        <div class="mt-2">
            <label for="doot-header-row" class="form-label fw-bold">Header row</label>
            <input type="number" id="doot-header-row" class="form-control" style="width:100px;"
                   min="1" value="1">
            <div id="doot-header-preview" class="mt-2 text-muted small"></div>
            <div class="text-muted small" style="margin:2px 0 10px">
                If the <i>columns found</i> are not the headers, adjust the header row until the
                column headers are displayed.
            </div>
            <button id="doot-step1-next" class="btn btn-primary mt-2">Next &rarr;</button>
        </div>
    </div>
</div>

<!-- Step 2: Identifier column -->
<div id="doot-step-2" class="d-none">
    <p class="fw-bold">Select the column that contains the unique identifier used for filtering:</p>
    <select id="doot-id-column" class="form-select" style="max-width:400px;"></select>
    <div class="mt-3">
        <button id="doot-step2-back" class="btn btn-secondary me-2">&larr; Back</button>
        <button id="doot-step2-next" class="btn btn-primary">Next &rarr;</button>
    </div>
</div>

<!-- Step 3: Exclude / Include lists -->
<div id="doot-step-3" class="d-none">
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="doot-exclude" class="form-label fw-bold">
                Exclude — rows whose identifier is in this list will be <em>removed</em> (one per line)
            </label>
            <textarea id="doot-exclude" class="form-control" rows="8"
                      placeholder="One identifier per line"></textarea>
        </div>
        <div class="col-md-6 mb-3">
            <label for="doot-include" class="form-label fw-bold">
                Include — only rows whose identifier is in this list will be <em>kept</em> (one per line)
            </label>
            <textarea id="doot-include" class="form-control" rows="8"
                      placeholder="One identifier per line"></textarea>
        </div>
    </div>
    <p class="text-muted small">
        If both lists are filled, <em>exclude</em> is applied first — any row whose identifier
        appears in the exclude list is removed, even if that identifier also appears in the
        include list.
    </p>
    <p class="text-muted small">
        <i class="fas fa-lock me-1"></i>
        Processing happens entirely on your device — no data is sent to REDCap until you
        click <strong>Upload</strong> in the next step.
    </p>
    <button id="doot-step3-back" class="btn btn-secondary me-2">&larr; Back</button>
    <button id="doot-process-btn" class="btn btn-primary">Process</button>
</div>

<!-- Step 4: Results + upload -->
<div id="doot-step-4" class="d-none">
    <div id="doot-results-msg" class="alert alert-info"></div>
    <p>
        <a id="doot-preview-link" href="#" download>Preview / save processed file</a>
    </p>
    <div class="mb-3" id="doot-record-section">
        <label for="doot-record-select" class="form-label">Upload to record</label>
        <select id="doot-record-select" class="form-select" style="max-width:20rem;">
            <option value="">Loading records&hellip;</option>
        </select>
    </div>
    <p class="text-muted small mb-2">
        <i class="fas fa-cloud-upload-alt me-1"></i>
        Clicking <strong>Upload to REDCap</strong> will send the processed file to the server.
    </p>
    <button id="doot-step4-back" class="btn btn-secondary me-2">&larr; Back</button>
    <button id="doot-upload-btn" class="btn btn-success" disabled>Upload to REDCap</button>
    <div id="doot-upload-progress" class="mt-2" style="display:none;">
        <span class="spinner-border spinner-border-sm" role="status"></span>
        Uploading&hellip;
    </div>
</div>

<!-- Step 5: Done -->
<div id="doot-step-5" class="d-none">
    <div id="doot-done-msg" class="alert alert-success"></div>
    <button id="doot-restart-btn" class="btn btn-primary">Process Another File</button>
</div>

<script type="text/javascript">
    $('#center').css('padding-right','20px')
    window.dootModule = <?= $jsModuleName ?>;
</script>
<script type="text/javascript" src="<?= $module->getUrl('process.js') ?>"></script>
