# scripts/main.py

import fitparse
import pandas as pd
from scripts.data_processing import DataProcessor
from scripts.plotting import DataPlotter
from scripts import FIELD_MAPPINGS

def main():
    fitfile = fitparse.FitFile('../data/session.fit')  # Replace with your actual .fit file path

    data = {'timestamp': [], 'power': [], 'smo2': [], 'heart_rate': [], 'thb': []}

    for record in fitfile.get_messages('record'):
        record_data = record.get_values()

        # Ensure using FIELD_MAPPINGS to access correct field names
        if all(field in record_data for field in FIELD_MAPPINGS.values()):
            data['timestamp'].append(record_data[FIELD_MAPPINGS['timestamp']])
            data['power'].append(record_data[FIELD_MAPPINGS['power']])
            data['smo2'].append(record_data[FIELD_MAPPINGS['smo2']])
            data['heart_rate'].append(record_data[FIELD_MAPPINGS['hr']])  # Use 'heart_rate' as the key
            data['thb'].append(record_data[FIELD_MAPPINGS['thb']])
        else:
            missing_fields = [field for field in FIELD_MAPPINGS.values() if field not in record_data]
            print(f"Skipping record, missing fields: {missing_fields}")

    df = pd.DataFrame(data)

    print("DataFrame columns:", df.columns)  # Debug: Print DataFrame columns
    print("First few rows of the DataFrame:\n", df.head())  # Debug: Print first few rows of DataFrame

    processor = DataProcessor(df)
    df_processed, work_intervals, slopes = processor.process()  # Get work_intervals and slopes here

    plotter = DataPlotter(df_processed, work_intervals=work_intervals, slopes=slopes)  # Pass slopes

    # Define start_time and end_time (in minutes), pass -1 to use full range
    start_time = 10  # Use -1 to indicate no zoom (full range)
    end_time = 60  # Use -1 to indicate no zoom (full range)
    plotter.plot_data(start_time=start_time, end_time=end_time)

if __name__ == "__main__":
    main()
