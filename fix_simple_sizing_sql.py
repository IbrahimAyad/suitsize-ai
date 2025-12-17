#!/usr/bin/env python3
"""
Fix SQL syntax for proper comma-separated VALUES
"""

import csv

def generate_fixed_simple_sizing_sql():
    """Generate properly formatted SQL with commas between VALUES"""
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
            height_parts = row['height_range_inches'].split('-')
            weight_parts = row['weight_range_lbs'].split('-')
            
            height_min = int(height_parts[0])
            height_max = int(height_parts[1])
            weight_min = int(weight_parts[0])
            weight_max = int(weight_parts[1])
            
            value_line = f"    ({height_min}, {height_max}, {weight_min}, {weight_max}, '{row['fit_style']}', '{row['body_type']}', '{row['recommended_size']}', {row['confidence_score']})"
            values.append(value_line)
    
    # Join values with commas
    sql_lines.append(',\n'.join(values))
    sql_lines.append(";")
    
    return '\n'.join(sql_lines)

def main():
    # Generate fixed simple sizing SQL
    fixed_sql = generate_fixed_simple_sizing_sql()
    with open('/workspace/import_simple_sizing_fixed.sql', 'w') as f:
        f.write(fixed_sql)
    
    print("✅ Generated fixed SQL file: import_simple_sizing_fixed.sql")

if __name__ == "__main__":
    main()
