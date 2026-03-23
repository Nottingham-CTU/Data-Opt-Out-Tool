# Data Opt-Out Tool — REDCap External Module

A REDCap external module that removes rows from a CSV file for participants/patients who have opted
out of data collection. Filtering happens entirely on the user's device, so that personal or
confidential data is not processed on the REDCap server until opt-outs have been removed. This
ensures compliance with legislation such as the GDPR and the NHS act in the UK (and similar
legislation worldwide).

---

## Usage

### Overview
The tool presents a 'wizard' that lets you:

- Load a CSV file from your device
- Identify which row contains the column headers and which column holds the unique identifier (e.g.
  NHS number, hospital number)
- Paste two optional filter lists — one for identifiers to **exclude** (rows to remove) and one for
  identifiers to **include** (all other rows are removed)
- Process the file in-browser and see how many rows were removed and how many remain
- Optionally preview or download the filtered file, then upload it directly to REDCap

All CSV parsing and filtering happens locally in your browser.<br>
**No participant data is sent to the server until you click *Upload to REDCap*.**

### Prerequisites
- The module must be enabled for your REDCap project by a system administrator.
- Your REDCap user account must be assigned a role that has been granted access to the tool
  (configured by an admin in the module's project settings).
- The field the uploaded files will be stored in must be in a repeating form or a repeating event,
  each upload will create a new instance.
- Each row containing personal/confidental data must be able to be uniquely identified by the value
  of a single column.
- Only CSV files are currently supported.

### Step-by-step
**Step 1 — Select file and header row**

1.  Open your REDCap project and click **Process Opt-Outs** in the left sidebar.
2.  Click **Select CSV file** and choose your file (maximum 20 MB).
3.  A preview of the first few column names appears. If your header is not on row 1, adjust the
    **Header row** number until the correct column names are shown.
4.  Click **Next**.

**Step 2 — Choose the identifier column**

5.  Select the column that contains the unique participant identifier used for filtering<br>
    (e.g. `nhs_number`, `participant_id`).
6.  Click **Next**.

**Step 3 — Enter filter lists and process**

7.  Optionally paste identifiers into one or both text boxes (one identifier per line):
    - **Exclude** — rows whose identifier appears here are **removed**.
    - **Include** — only rows whose identifier appears here are **kept**; all others are removed.
    - If both lists are filled, Exclude is applied first. A row appearing in both lists will be removed.
8.  If neither list is filled you will be asked to confirm that you want to keep all rows.
9.  Click **Process**. All filtering runs in your browser — nothing is sent to the server at this point.

**Step 4 — Review results and upload**

10. The tool reports how many rows were removed and how many remain.
11. Click **Preview / save processed file** to inspect or save a local copy.
12. When satisfied, click **Upload to REDCap**. The processed file is sent to the server and saved
    in a new instance of the configured repeating event/form.
13. A success message confirms the record the file was saved against.
14. Optionally, click **Process Another File** to start again from Step 1.

---

## Module Setup

### Enabling the module
REDCap administrators can enable the module through **Control Centre → External Modules** in the
usual way. When enabled on a project, the *Process Opt-Outs* sidebar link and project settings will
become available.

### Project settings

#### Instructions / User Access
- **Custom instruction text**<br>
  Optionally include some instructions to be displayed to users at the start of the process.<br>
  HTML `<a href="...">`, `<b>` and `<i>` tags are supported.
- **Custom instruction style**<br>
  Choose the style for the *custom instruction text*: information (blue box with **i** icon) or
  warning (yellow box with warning icon).
- **Process role(s)**<br>
  Select each user role that should be allowed to access the Process Opt-Outs page and perform
  uploads. REDCap administrators always have access regardless of this setting.

#### Record Selection
Users will only see records which are in their DAG. Users not assigned to a DAG will see all records
(subject to filtering).

- **Record label field**<br>
  The value of this field will be shown to the user when selecting the record to upload to.
- **Filter records by label field**<br>
  If selected, will only include records which have a value for the *record label field*.

#### Field Selection
Configures where uploaded files are stored. This must be a field within a repeating event or form.
The file is always saved in a **new** repeat instance of the event/form.

- **Repeat type**
  - **Classic: repeating form** — classic project with a repeating instrument
  - **Longitudinal: repeating event** — longitudinal project where the entire event repeats
  - **Longitudinal: repeating form** — longitudinal project where a single instrument within an
    event repeats
