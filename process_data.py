import csv
import os

def process_csv_files():
    input_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv',
        'data/daily_sales_data_2.csv'
    ]
    
    output_rows = []
    
    # Process each file
    for file in input_files:
        if not os.path.exists(file):
            print(f"Warning: {file} not found")
            continue
            
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            # Strip whitespace from column names
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
            for row in reader:
                # Create a new dict with stripped keys
                clean_row = {k.strip(): v.strip() for k, v in row.items()}
                # Strip whitespace from keys and values
                product = clean_row['product'].lower()
                
                # Filter for pink morsel only
                if product == 'pink morsel':
                    # Extract price and quantity
                    price_str = clean_row['price'].replace('$', '')
                    price = float(price_str)
                    quantity = int(clean_row['quantity'])
                    
                    # Calculate sales
                    sales = price * quantity
                    
                    # Extract date and region
                    date = clean_row['date']
                    region = clean_row['region']
                    
                    output_rows.append({
                        'sales': sales,
                        'date': date,
                        'region': region
                    })
    
    # Write output file
    output_file = 'data/formatted_sales_data.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['sales', 'date', 'region'])
        writer.writeheader()
        writer.writerows(output_rows)
    
    print(f"Processing complete!")
    print(f"Total rows in output: {len(output_rows)}")
    print(f"Output saved to: {output_file}")
    
    # Display first few rows
    print("\nFirst 5 rows of output:")
    for i, row in enumerate(output_rows[:5]):
        print(f"  {row}")

if __name__ == '__main__':
    process_csv_files()
