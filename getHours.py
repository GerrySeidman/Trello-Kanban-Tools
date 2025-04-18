import json
import re
import os
import csv
import sys
from collections import defaultdict

def extract_time_entries_to_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        trello_data = json.load(file)
    
    cards = trello_data.get('cards', [])
    
    valid_names = ["Mahin", "Ahmed", "Med", "Indranil", "Joe", "Don", "Michael", "Test"]
    pattern = r'(?:\*\*)?Sprint\s+([\d/]+)\s+\((' + '|'.join(valid_names) + r')\):\s+(\d*\.?\d+)\s+(hours?)(?:\*\*)?'
    
    result = []
    all_entries = []
    summary_by_sprint = defaultdict(lambda: defaultdict(float))

    for card in cards:
        card_name = card.get('name', 'Unnamed Card')
        card_id = card.get('id', '')
        description = card.get('desc', '')
        
        matches = re.findall(pattern, description)
        
        time_entries = []
        
        for match in matches:
            date, name, hours, hour_text = match
            hours_float = float(hours)
            
            if description.find(f"**Sprint {date}") >= 0 or description.find(f"{hours} {hour_text}**") >= 0:
                formatted_entry = f"**Sprint {date} ({name}): {hours} {hour_text}**"
            else:
                formatted_entry = f"Sprint {date} ({name}): {hours} {hour_text}"
            time_entries.append(formatted_entry)
            
            all_entries.append({
                "card_id": card_id,
                "card_name": card_name,
                "person": name,
                "hours": hours_float,
                "date": date
            })
            
            summary_by_sprint[date][name] += hours_float
        
        if time_entries:
            card_data = {
                "id": card_id,
                "name": card_name,
                "times": time_entries
            }
            result.append(card_data)
    
    time_entries_dir = "time_entries"
    
    if not os.path.exists(time_entries_dir):
        os.makedirs(time_entries_dir)
    else:
        for file in os.listdir(time_entries_dir):
            file_path = os.path.join(time_entries_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    
    output = json.dumps(result, indent=2)
    output_path = os.path.join(time_entries_dir, "time_entries.json")
    with open(output_path, "w", encoding='utf-8') as outfile:
        outfile.write(output)
    
    sheets_path = os.path.join(time_entries_dir, "time_entries_for_sheets.csv")
    with open(sheets_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['Card ID', 'Card Name', 'Person', 'Hours', 'Date'])
        
        for entry in all_entries:
            writer.writerow([
                entry["card_id"], 
                entry["card_name"], 
                entry["person"], 
                entry["hours"], 
                entry["date"]
            ])
        
        writer.writerow([])
        writer.writerow(["SUMMARY STATISTICS"])
        writer.writerow([])
        
        writer.writerow(["Sprint", "Person", "Total Hours"])
        
        for sprint, person_hours in sorted(summary_by_sprint.items()):
            for person, hours in sorted(person_hours.items()):
                writer.writerow([sprint, person, hours])
        
        writer.writerow([])
        writer.writerow(["PERSON TOTALS"])
        writer.writerow([])
        
        person_totals = defaultdict(float)
        for sprint, person_hours in summary_by_sprint.items():
            for person, hours in person_hours.items():
                person_totals[person] += hours
        
        writer.writerow(["Person", "Total Hours"])
        for person, hours in sorted(person_totals.items()):
            writer.writerow([person, hours])
        
        writer.writerow([])
        writer.writerow(["SPRINT TOTALS"])
        writer.writerow([])
        
        sprint_totals = defaultdict(float)
        for sprint, person_hours in summary_by_sprint.items():
            for person, hours in person_hours.items():
                sprint_totals[sprint] += hours
        
        writer.writerow(["Sprint", "Total Hours"])
        for sprint, hours in sorted(sprint_totals.items()):
            writer.writerow([sprint, hours])
    
    print(f"Time entries saved to:")
    print(f"  - JSON: {output_path}")
    print(f"  - CSV: {sheets_path}")

if __name__ == "__main__":
    file_path = "./data.json"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    extract_time_entries_to_json(file_path)