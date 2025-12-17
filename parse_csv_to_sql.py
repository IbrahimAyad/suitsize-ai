#!/usr/bin/env python3
"""
Parse CSV files and generate SQL insert statements for Supabase import
"""

import csv
import json

def parse_height_range(height_str):
    """Parse height range like '63-66' into min/max"""
    parts = height_str.split('-')
    return int(parts[0]), int(parts[1])

def parse_weight_range(weight_str):
    """Parse weight range like '110-125' into min/max"""
    parts = weight_str.split('-')
    return int(parts[0]), int(parts[1])

def generate_simple_sizing_sql():
    """Generate SQL for simple sizing lookup data"""
    sql_lines = ["-- Import simple sizing lookup data"]
    sql_lines.append("-- Generated from simple_sizing_lookup.csv")
    sql_lines.append("")
    sql_lines.append("INSERT INTO sizing_lookup_simple (")
    sql_lines.append("    height_min_inches, height_max_inches,")
    sql_lines.append("    weight_min_lbs, weight_max_lbs,")
    sql_lines.append("    fit_style, body_type, recommended_size, confidence_score")
    sql_lines.append(") VALUES")
    
    values = []
    
    with open('/workspace/simple_sizing_lookup.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            height_min, height_max = parse_height_range(row['height_range_inches'])
            weight_min, weight_max = parse_weight_range(row['weight_range_lbs'])
            
            value_line = f"    ({height_min}, {height_max}, {weight_min}, {weight_max}, '{row['fit_style']}', '{row['body_type']}', '{row['recommended_size']}', {row['confidence_score']})"
            values.append(value_line)
    
    sql_lines.extend(values)
    sql_lines.append(";")
    
    return '\n'.join(sql_lines)

def generate_detailed_sizing_sql():
    """Generate SQL for detailed measurements data"""
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
            # Parse body_type_adjustments JSON
            adjustments = row['body_type_adjustments'].replace('"', '\"')
            
            value_line = f"""    ('{row['size']}', {row['jacket_size']}, '{row['length_type']}',
        {row['height_min_inches']}, {row['height_max_inches']},
        {row['weight_min_lbs']}, {row['weight_max_lbs']},
        {row['chest_min_inches']}, {row['chest_max_inches']},
        {row['waist_min_inches']}, {row['waist_max_inches']},
        {row['shoulder_inches']}, {row['sleeve_inches']}, {row['jacket_length_inches']},
        {row['drop_inches']}, {row['pant_waist_inches']},
        {row['confidence_score']}, '{adjustments}')"""
            values.append(value_line)
    
    sql_lines.extend(values)
    sql_lines.append(";")
    
    return '\n'.join(sql_lines)

def main():
    # Generate simple sizing SQL
    simple_sql = generate_simple_sizing_sql()
    with open('/workspace/import_simple_sizing.sql', 'w') as f:
        f.write(simple_sql)
    
    # Generate detailed sizing SQL  
    detailed_sql = generate_detailed_sizing_sql()
    with open('/workspace/import_detailed_sizing.sql', 'w') as f:
        f.write(detailed_sql)
    
    print("✅ Generated SQL files:")
    print("  - import_simple_sizing.sql")
    print("  - import_detailed_sizing.sql")

if __name__ == "__main__":
    main()
