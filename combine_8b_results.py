import os
import json

def combine_json_files(input_folder, output_file):
    """
    Combines all JSON files in a specified folder into one JSON file.

    Parameters:
        input_folder (str): Path to the folder containing JSON files.
        output_file (str): Path to the output combined JSON file.
    """
    combined_data = []

    # Iterate through all files in the given folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):  # Only process JSON files
            file_path = os.path.join(input_folder, filename)
            
            # Read and load the JSON file
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    if isinstance(data, list):  # If the JSON is a list, extend the combined list
                        combined_data.extend(data)
                    else:  # If the JSON is a dictionary, append it to the combined list
                        combined_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {filename}: {e}")
                continue

    # Write the combined JSON data to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as output_json_file:
            json.dump(combined_data, output_json_file, indent=4, ensure_ascii=False)
        print(f"Combined JSON saved to {output_file}")
    except Exception as e:
        print(f"Error writing combined JSON to file: {e}")


# Example usage:
if __name__ == "__main__":
    input_folder = "results-llama3.1-8b"  # Replace with your folder path
    output_file = "combinedresults-llama3.1-8b.json"  # Replace with your desired output file path
    combine_json_files(input_folder, output_file)