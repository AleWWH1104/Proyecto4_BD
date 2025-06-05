# app/utils.py
import csv
from io import StringIO

def export_to_csv(data, fieldnames, filename=None):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for item in data:
        if isinstance(item, dict):
            writer.writerow(item)
        else:
            writer.writerow(item.__dict__)
    
    if filename:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            f.write(output.getvalue())
        return filename
    else:
        return output.getvalue()