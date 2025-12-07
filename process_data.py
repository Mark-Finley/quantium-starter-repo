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
            for row in reader:
                # Strip whitespace from keys and values
                product = row['product'].strip().lower()
                
                # Filter for pink morsel only
                if product == 'pink morsel':
                    # Extract price and quantity
                    price_str = row['price'].strip().replace('$', '')
                    price = float(price_str)
                    quantity = int(row['quantity'].strip())
                    
                    # Calculate sales
                    sales = price * quantity
                    
                    # Extract date and region
                    date = row['date'].strip()
                    region = row['region'].strip()
                    
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
