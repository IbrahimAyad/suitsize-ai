#!/usr/bin/env python3
"""
Fix JSON format for body_type_adjustments field
"""

import csv
import json

def fix_json_format():
    """Fix JSON format and generate proper SQL"""
    
    with open('/workspace/suitsize_47_sizes_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        
        print("Sample of fixed data:")
        for i, row in enumerate(reader):
            if i < 3:  # Show first 3 rows as sample
                # Parse and fix the JSON
                raw_json = row['body_type_adjustments']
                
                # Fix the JSON format by replacing + with just the number
                fixed_json = raw_json.replace('+1.0', '1.0').replace('+0.5', '0.5').replace('-1.0', '-1.0')
                
                print(f"Row {i+1}:")
                print(f"  Raw: {raw_json}")
                print(f"  Fixed: {fixed_json}")
                print()
            else:
                break

if __name__ == "__main__":
    fix_json_format()
