# Auristor Intern Trello Time Entry Extractor

This tool extracts time entries from a Trello board JSON export and generates formatted summary reports. It's designed to help teams track time spent on tasks across sprints.

## Getting Started

### Step 1: Download the Trello Board JSON

You will have to manually download the Trello board (as JSON):

1. Open your Trello board
2. Click on "Show Menu" (top-right corner)
3. Click "More"
4. Select "Print and Export"
5. Choose "Export as JSON"
6. Save the file locally (IMPORTANT: rename to `data.json`)

### Step 2: Install Requirements

This script requires Python 3.6+ and standard libraries that come with Python (no additional installation required):

- json
- re
- os
- csv
- sys
- collections

### Step 3: Run the Script

Place the script and your downloaded JSON file in the same directory, then run:

```bash
python getHours.py
```

Or specify a custom path to the JSON file:

```bash
python getHours.py path/to/your/trello_export.json
```

## How It Works

The script looks for time entries in the following format in card descriptions:

```
Sprint 4/7 (Mahin): 2 hours
```

Valid variations include:

- With or without bold formatting: `**Sprint 4/7 (Mahin): 2 hours**`
- Different hour formats: `0.5 hours`, `.5 hours`, `1.5 hours`, `1 hour`
- Different sprints (e.g., `3/24`, `4/7`)
- Different team members specified in the valid names list

## Output

The script generates two files in a `time_entries` directory:

1. **time_entries.json** - A JSON file containing:

   - Card ID
   - Card name
   - Time entries found in each card

2. **time_entries_for_sheets.csv** - A CSV file for Google Sheets with:
   - Individual time entries (Card ID, Card Name, Person, Hours, Date)
   - Summary statistics by sprint and person
   - Total hours per person
   - Total hours per sprint

## Configuring Valid Names

Edit the `valid_names` list in the script to add or remove team members:

```python
valid_names = ["Mahin", "Ahmed", "Med", "Indranil", "Joe", "Don", "Michael", "Test"]
```

## Example Output

### JSON Output Format:

```json
[
	{
		"id": "67cdafe55ebb3d95a8073f37",
		"name": "Move the \"Refresh Data\" and \"Remove Filters\" buttons",
		"times": ["**Sprint 4/7 (Mahin): 2 hours**"]
	},
	{
		"id": "67d6e5e52b1c72a3d82f4996",
		"name": "Set up play.iamx.com AuriStorFS Cell",
		"times": ["Sprint 3/24 (Don): 4 hours"]
	}
]
```

### CSV Output Structure:

The CSV file contains:

1. **Task details section** - All individual time entries
2. **Sprint summaries section** - Hours by sprint and person
3. **Person totals section** - Total hours per person across all sprints
4. **Sprint totals section** - Total hours per sprint across all people

## Importing into Google Sheets

1. Open Google Sheets
2. File > Import
3. Upload > Select the CSV file
4. Import location: Replace spreadsheet or Insert new sheet
5. Import type: "Detect automatically"
6. Click "Import data"

## Troubleshooting

If time entries aren't being detected:

1. Ensure they strictly follow the format: `Sprint 4/7 (Person): X hours`
2. Check that the person's name is in the `valid_names` list
3. Verify there is a space between the hour value and the word "hour" or "hours"
