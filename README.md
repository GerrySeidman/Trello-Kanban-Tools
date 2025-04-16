# Trello Kanban Board: Intern Project Management

This README explains how we use the free version of Trello as a Kanban board for our project management and time tracking.

## Using Trello as a Kanban Board

[Trello](https://trello.com) is a flexible project management tool that works perfectly as a Kanban board. The free version offers:

- Unlimited cards and lists
- Basic automation
- Basic power-ups
- Easy drag-and-drop functionality
- Card-level commenting and activity logging
- File attachments (up to 10MB per attachment)
- Labels and due dates

Our team uses Trello to visualize workflow, limit work in progress, and track time spent on tasks across sprints.

## Card Structure

Each card in our Trello board follows a specific structure to ensure consistency and proper time tracking:

### Card Description Format

Each card description should contain the following sections:

#### 1. Time Estimate

- Initial estimate of how long the task will take
- Example: `Estimated time: 4 hours`

#### 2. Sprint Time Entries

- Format: `**Sprint <date> (<name>): <hours> hours**`
- Example: `**Sprint 4/7 (Mahin): 2 hours**`
- Can include multiple entries from different team members or sprints
- Bold formatting is optional but recommended for visibility

#### 3. GitHub Branch

- Link to the associated GitHub branch
- Example: `Branch: https://github.com/username/repo/tree/feature-branch`

#### 4. Description

- Detailed description of the task
- Requirements and acceptance criteria
- Any other relevant information

### Subtasks Checklist

Break down complex tasks into subtasks using Trello's checklist feature:

- Click "Add checklist" on the card
- Add individual items that need to be completed
- Check off items as they are completed

### Reviewers Checklist

We use a second checklist specifically for code reviews:

#### Reviewer Assignment

- We use Trello's labels to indicate assigned reviewers
- Each team member has a designated color label
- Apply the label to the card to assign a reviewer

#### Review Process

1. Reviewer checks their name in the checklist when they've reviewed
2. Reviewer adds a comment with their feedback:
   - "Looks good" - Approved without changes
   - "Needs improvement" (with details) - Minor issues to address
   - "Has problems/bugs" (with details) - Major issues requiring fixes

### Comments

All feedback, including review feedback, is provided as comments on the card:

- Comments maintain a chronological history of discussion
- Use @mentions to notify specific team members
- Attach screenshots or files to illustrate points
- Reply to specific comments to maintain context

## Swim Lanes (Lists)

Our board is organized into the following swim lanes (lists):

1. **Backlog** - Tasks that are defined but not yet prioritized for a sprint
2. **To Do** - Tasks prioritized for the current sprint
3. **In Progress** - Tasks currently being worked on (limit: 1-2 per person)
4. **Review** - Tasks completed and awaiting code review
5. **Done** - Tasks fully completed and approved
6. **Blocked** - Tasks that cannot proceed due to dependencies or issues

## Time Tracking

We use the card description to track time entries in a structured format that can be extracted using our time entry tool. This allows us to:

- Track hours spent per person per sprint
- Generate reports for time allocation
- Analyze productivity and effort
- Plan future sprints more accurately

The time entry extractor tool parses these entries from the Trello JSON export and generates summary reports.

## Workflow

1. Tasks start in the **Backlog**
2. During sprint planning, tasks are prioritized and moved to **To Do**
3. When work begins, the card is moved to **In Progress**
4. Upon completion, the developer:
   - Adds their time entry in the proper format
   - Moves the card to **Review**
   - Applies reviewer labels
5. Reviewers check their name and provide feedback
6. If changes are needed, the card returns to **In Progress**
7. When approved, the card moves to **Done**
8. If blocked, cards move to the **Blocked** lane with a comment explaining why

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
