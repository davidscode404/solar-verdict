import pandas as pd

def calculate_weather_averages(csv_file_path, output_file_path='weather_summary.txt'):
    try:
        df = pd.read_csv(csv_file_path)
        
        # Print to console as before
        print(f"Average air temperature: {df['air_temp'].mean():.2f}")
        print(f"Average DNI: {df['dni'].mean():.2f}")
        print(f"Average GHI: {df['ghi'].mean():.2f}")
        
        # Create the summary text
        summary = f"This location has an annual average of {df['air_temp'].mean():.2f} air temperature, {df['dni'].mean():.2f} DNI and {df['ghi'].mean():.2f} GHI. How much money and energy could one save by installing solar panels?"
        
        # Write to file
        with open(output_file_path, 'w') as f:
            f.write(summary)
            
        print(f"\nSummary has been saved to {output_file_path}")
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
calculate_weather_averages('weather_data.csv')