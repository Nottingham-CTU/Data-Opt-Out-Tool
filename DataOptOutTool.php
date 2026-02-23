<?php

namespace Nottingham\DataOptOutTool;

use ExternalModules\AbstractExternalModule;
use REDCap;

class DataOptOutTool extends AbstractExternalModule
{
    /**
     * Module framework hook: handles AJAX requests.
     *
     * @param string $action The AJAX action name.
     * @param array $payload Associative array of data sent with the request.
     * @param int $project_id Current REDCap project ID.
     * @param string $group_id Data Access Group ID for the current user (or 'admin').
     * @return array{success: bool, error?: string}
     */
    public function redcap_module_ajax($action, $payload, $project_id, $record, $instrument, $event_id, $repeat_instance, $survey_hash, $response_id, $survey_queue_hash, $queue_id, $survey_mailing_id, $group_id)
    {
        if (!$this->userIsAuthorised()) {
            return ['success' => false, 'error' => 'Access denied'];
        }

        if ($action === 'upload-file') {
            return $this->handleUploadFile($payload, $project_id, $group_id);
        }

        if ($action === 'get-records') {
            return $this->handleGetRecords($project_id);
        }

        return ['success' => false, 'error' => 'Unknown action'];
    }

    /**
     * Module framework hook: controls whether this module's sidebar link is shown.
     *
     * @param int $project_id Current REDCap project ID.
     * @param array $link The link configuration array provided by the framework.
     * @return array|null The link array to show it, or null to hide it.
     */
    public function redcap_module_link_check_display($project_id, $link)
    {
        return $this->userIsAuthorised() ? $link : null;
    }

    /**
     * Returns true if the current user may access the module's page and AJAX endpoints.
     *
     * Admins are always authorized. For other users, access is granted when their
     * assigned role ID appears in the `process-roles` project setting.
     *
     * @return bool True if the current user is authorized, false otherwise.
     */
    private function userIsAuthorised(): bool
    {
        $user = $this->getUser();
        if ($user->isSuperUser()) return true;
        $rights = $user->getRights();
        $userRoleId = $rights['role_id'] ?? null;
        if (empty($userRoleId)) return false;
        $allowedRoles = $this->getProjectSetting('process-roles') ?? [];
        return in_array($userRoleId, (array)$allowedRoles, false);
    }

    /**
     * Handles the `get-records` AJAX action.
     *
     * Returns all record IDs in the project (classic) or only those with data
     * in the configured event (longitudinal), sorted alphabetically.
     *
     * @param int $project_id The REDCap project ID.
     * @return array{success: bool, records?: string[], error?: string}
     */
    private function handleGetRecords($project_id)
    {
        $target = $this->getSubSettings('upload-target');
        $uploadMode = $target[0]['upload-mode'] ?? null;

        if (empty($uploadMode)) {
            return ['success' => false, 'error' => 'Upload target not configured (missing Repeat type)'];
        }

        $labelField = $this->getProjectSetting('record-label-field');
        $filterByLabel = $this->getProjectSetting('record-label-filter');

        $fields = [REDCap::getRecordIdField()];
        if (!empty($labelField)) {
            $fields[] = $labelField;
        }

        $params = [
            'project_id' => $project_id,
            'fields' => $fields,
        ];

        if (!empty($labelField) && $filterByLabel) {
            $params['filterLogic'] = "[{$labelField}] <> ''";
        }

        $data = REDCap::getData($params);

        $recordIds = [];
        $recordLabels = [];
        foreach ($data as $recordId => $eventData) {
            $recordIds[] = (string)$recordId;
            if (!empty($labelField)) {
                foreach ($eventData as $eventValues) {
                    $val = $eventValues[$labelField] ?? '';
                    if ($val !== '' && $val !== null) {
                        $recordLabels[(string)$recordId] = (string)$val;
                        break;
                    }
                }
            }
        }
        $recordIds = array_unique($recordIds);
        sort($recordIds);

        return ['success' => true, 'records' => array_values($recordIds), 'labels' => $recordLabels];
    }

    /**
     * Handles the `upload-file` AJAX action.
     *
     * @param array $payload Must contain `file_content` base64 string, `filename`, and `record_id`.
     * @param int $project_id The REDCap project ID to save the file into.
     * @param string $group_id The current user's DAG ID, or 'admin'.
     * @return array{success: bool, error?: string, record?: string}
     */
    private function handleUploadFile($payload, $project_id, $group_id)
    {
        $fileContent = $payload['file_content'] ?? null;
        $filename = $payload['filename'] ?? null;

        if (empty($fileContent) || empty($filename)) {
            return ['success' => false, 'error' => 'Missing file_content or filename'];
        }

        // Base64 string is ~4/3 the raw size; so 20 MB raw ≈ 26.7 MB base64
        if (strlen($fileContent) > 26_700_000) {
            return ['success' => false, 'error' => 'File too large (maximum 20 MB)'];
        }

        // Sanitize filename — strip directory traversal, keep only safe characters
        $filename = basename(preg_replace('/[^A-Za-z0-9._\-]/', '_', $filename));
        if ($filename === '') {
            $filename = 'upload.csv';
        }

        $decoded = base64_decode($fileContent, true);
        if ($decoded === false) {
            return ['success' => false, 'error' => 'Invalid base64 in file_content'];
        }

        $target = $this->getSubSettings('upload-target');
        $uploadMode = $target[0]['upload-mode'] ?? null;
        $uploadField = $target[0]['upload-field'] ?? null;
        $uploadEvent = $target[0]['upload-event'] ?? null;
        $uploadForm = $target[0]['upload-form'] ?? null;

        $uploadRecord = $payload['record_id'] ?? null;
        if (empty($uploadRecord)) {
            return ['success' => false, 'error' => 'No record ID provided'];
        }

        $missing = [];
        if (empty($uploadMode)) $missing[] = 'Repeat type';
        if (empty($uploadField)) $missing[] = 'Upload Field';
        if (in_array($uploadMode, ['longitudinal-event', 'longitudinal-form'], true) && empty($uploadEvent)) {
            $missing[] = 'Repeating Event';
        }
        if (in_array($uploadMode, ['classic-form', 'longitudinal-form'], true) && empty($uploadForm)) {
            $missing[] = 'Repeating Form';
        }

        if (!empty($missing)) {
            return ['success' => false, 'error' => 'Upload target not configured. Missing settings: ' . implode(', ', $missing)];
        }

        $existingRecord = REDCap::getData([
            'project_id' => $project_id,
            'records' => [$uploadRecord],
            'fields' => [REDCap::getRecordIdField()],
        ]);
        if (empty($existingRecord)) {
            return ['success' => false, 'error' => 'Selected upload record does not exist'];
        }

        $tmpPath = $this->createTempFile();
        file_put_contents($tmpPath, $decoded);

        $edocId = REDCap::storeFile($tmpPath, $project_id, $filename);
        if (empty($edocId)) {
            return ['success' => false, 'error' => 'Failed to save file to REDCap storage'];
        }

        $data = [
            REDCap::getRecordIdField() => $uploadRecord,
            'redcap_repeat_instance' => 'new',
            $uploadField => $edocId,
            'redcap_data_access_group' => $group_id === 'admin' ? '' : $group_id,
        ];

        if (in_array($uploadMode, ['longitudinal-event', 'longitudinal-form'], true)) {
            $data['redcap_event_name'] = $uploadEvent;
        }
        if (in_array($uploadMode, ['classic-form', 'longitudinal-form'], true)) {
            $data['redcap_repeat_instrument'] = $uploadForm;
        }

        $result = REDCap::saveData([
            'project_id' => $project_id,
            'dataFormat' => 'json-array',
            'data' => [$data],
            'skipFileUploadFields' => false,
        ]);

        if (!empty($result['errors'])) {
            return ['success' => false, 'error' => implode('; ', (array)$result['errors'])];
        }

        return ['success' => true, 'record' => $uploadRecord];
    }
}
