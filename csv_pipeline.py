import csv
from pathlib import Path
import json

def json_folder_to_csv(folder_path, output_csv_path):
    """
    Reads all JSON files from a folder and converts them to a single CSV file.
    
    Args:
        folder_path (str): Path to the folder containing JSON files
        output_csv_path (str): Path where the output CSV file will be saved
    
    Returns:
        int: Number of JSON files processed
    """
    
    folder = Path(folder_path)
    json_files = list(folder.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in '{folder_path}'")
        return 0
    
    # Read first JSON to get column headers
    with open(json_files[0], 'r', encoding='utf-8') as f:
        first_data = json.load(f)
        column_headers = list(first_data.keys())
    
    # Write to CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_headers)
        writer.writeheader()
        
        # Process each JSON file
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                writer.writerow(data)
    
    print(f"Successfully created CSV: {output_csv_path}")
    print(f"Processed {len(json_files)} JSON files")
    
    return len(json_files)

if __name__ == "__main__":
    json_folder_to_csv("saved_json","professors.csv")