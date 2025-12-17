#!/usr/bin/env python3
"""
Generate properly formatted SQL for detailed sizing data with fixed JSON
"""

import csv
import json

def generate_detailed_sizing_sql_fixed():
    """Generate SQL for detailed measurements data with fixed JSON"""
    sql_lines = ["-- Import detailed sizing measurements data"]
    sql_lines.append("-- Generated from suitsize_47_sizes_data.csv")
    sql_lines.append("")
    sql_lines.append("INSERT INTO sizing_detailed_measurements (")
    sql_lines.append("    size, jacket_size, length_type,")
    sql_lines.append("    height_min_inches, height_max_inches,")
    sql_lines.append("    weight_min_lbs, weight_max_lbs,")
    sql_lines.append("    chest_min_inches, chest_max_inches,")
    sql_lines.append("    waist_min_inches, waist_max_inches,")
    sql_lines.append("    shoulder_inches, sleeve_inches, jacket_length_inches,")
    sql_lines.append("    drop_inches, pant_waist_inches,")
    sql_lines.append("    confidence_score, body_type_adjustments")
    sql_lines.append(") VALUES")
    
    values = []
    
    with open('/workspace/suitsize_47_sizes_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Fix the JSON format by replacing + signs
            raw_json = row['body_type_adjustments']
            fixed_json = raw_json.replace('+1.0', '1.0').replace('+0.5', '0.5').replace('-1.0', '-1.0')
            
            value_line = f"""    ('{row['size']}', {row['jacket_size']}, '{row['length_type']}',
        {row['height_min_inches']}, {row['height_max_inches']},
        {row['weight_min_lbs']}, {row['weight_max_lbs']},
        {row['chest_min_inches']}, {row['chest_max_inches']},
        {row['waist_min_inches']}, {row['waist_max_inches']},
        {row['shoulder_inches']}, {row['sleeve_inches']}, {row['jacket_length_inches']},
        {row['drop_inches']}, {row['pant_waist_inches']},
        {row['confidence_score']}, '{fixed_json}')"""
            values.append(value_line)
    
    sql_lines.append(',\n'.join(values))
    sql_lines.append(";")
    
    return '\n'.join(sql_lines)

def main():
    # Generate detailed sizing SQL with fixed JSON
    detailed_sql = generate_detailed_sizing_sql_fixed()
    with open('/workspace/import_detailed_sizing_fixed.sql', 'w') as f:
        f.write(detailed_sql)
    
    print("✅ Generated fixed SQL file: import_detailed_sizing_fixed.sql")

if __name__ == "__main__":
    main()
