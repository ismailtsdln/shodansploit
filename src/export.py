import json
import csv
import os
from datetime import datetime

class Exporter:
    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

    def export(self, data, filename=None, format="json"):
        """
        Export data to a file in the specified format.
        
        Args:
            data: The data to export (dict or list)
            filename: Optional filename. If not provided, generates a timestamped name.
            format: Export format ('json', 'csv', 'txt')
        
        Returns:
            str: Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shodan_export_{timestamp}.{format}"
        
        filepath = os.path.join(self.results_dir, filename)
        
        try:
            if format == "json":
                return self._export_json(data, filepath)
            elif format == "csv":
                return self._export_csv(data, filepath)
            elif format == "txt":
                return self._export_txt(data, filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")

    def _export_json(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

    def _export_csv(self, data, filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if isinstance(data, dict):
                # If it's a dict, try to find a list inside (e.g., 'matches' or 'results')
                if 'matches' in data:
                    data = data['matches']
                elif 'results' in data:
                    data = data['results']
                else:
                    # Convert single dict to list
                    data = [data]
            
            if not data or not isinstance(data, list):
                raise ValueError("CSV export requires list data")
            
            # Get all unique keys from all items
            fieldnames = set()
            for item in data:
                if isinstance(item, dict):
                    fieldnames.update(item.keys())
            
            fieldnames = sorted(fieldnames)
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in data:
                if isinstance(item, dict):
                    # Flatten nested structures
                    flattened = {}
                    for key, value in item.items():
                        if isinstance(value, (dict, list)):
                            flattened[key] = json.dumps(value)
                        else:
                            flattened[key] = value
                    writer.writerow(flattened)
        
        return filepath

    def _export_txt(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(data, (dict, list)):
                f.write(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                f.write(str(data))
        return filepath
