import os
import time
import pandas as pd
from datetime import datetime
from solcast import live, historic, forecast, tmy, pv_power_sites, aggregations
from solcast.unmetered_locations import UNMETERED_LOCATIONS

api_key = os.environ.get('SOLCAST_API_KEY')

sydney = UNMETERED_LOCATIONS['Sydney Opera House']
grand_canyon = UNMETERED_LOCATIONS['Grand Canyon']
stonehenge = UNMETERED_LOCATIONS['Stonehenge']
colosseum = UNMETERED_LOCATIONS['The Colosseum']
giza = UNMETERED_LOCATIONS['Giza Pyramid Complex']
taj_mahal = UNMETERED_LOCATIONS['Taj Mahal']
fort_peck = UNMETERED_LOCATIONS['Fort Peck']
goodwin_creek = UNMETERED_LOCATIONS['Goodwin Creek']

def get_info(the_input, output_filepath='weather_data.csv'):
    data = []
    start_date = '2023-01-01'
    start_dates = pd.date_range(start=start_date, periods=12, freq='MS')
    
    for start_day in start_dates:
        end_day = (start_day + pd.offsets.MonthEnd(1)).strftime('%Y-%m-%dT23:59:59.000Z')
        try:
            res = historic.radiation_and_weather(
                latitude=the_input['latitude'],
                longitude=the_input['longitude'],
                start=start_day,
                end=end_day,
            )
            data.append(res.to_pandas())
        except Exception as e:
            print(f"Request failed for start date {start_day}: {e}")
        # Delay between requests to avoid hitting the default historic rate limit
        time.sleep(1)
    
    # Combine all the data
    combined_data = pd.concat(data)
    
    try:
        # Save to CSV file
        combined_data.to_csv(output_filepath, index=True)
        print(f"Data successfully saved to {output_filepath}")
    except Exception as e:
        print(f"Error saving data to file: {e}")
    
    return combined_data

print(get_info(colosseum))
