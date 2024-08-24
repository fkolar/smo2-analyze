# scripts/data_parser.py

import fitparse
import pandas as pd
from scripts import FIELD_MAPPINGS

class DataParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_fit_file(self):
        fitfile = fitparse.FitFile(self.filepath)
        data = {'timestamp': [], 'power': [], 'smo2': [], 'hr': [], 'thb': []}

        print("Starting to parse .fit file...")

        for i, record in enumerate(fitfile.get_messages('record')):
            record_data = record.get_values()

            # Print the keys for the first few records to identify actual field names
            if i < 5:  # Limit to first 5 records to avoid excessive output
                print(f"Record {i+1} keys: {record_data.keys()}")

            # Check if all required fields are present
            fields_to_check = [
                FIELD_MAPPINGS['timestamp'],
                FIELD_MAPPINGS['power'],
                FIELD_MAPPINGS['smo2'],
                FIELD_MAPPINGS['hr'],
                FIELD_MAPPINGS['thb']
            ]

            # Check if fields are present in the record
            missing_fields = [field for field in fields_to_check if field not in record_data]
            if missing_fields:
                print(f"Skipping record, missing fields: {missing_fields}")
                continue

            # Append data only if all fields are present
            for key in data.keys():
                if FIELD_MAPPINGS[key] in record_data:
                    data[key].append(record_data[FIELD_MAPPINGS[key]])
                else:
                    data[key].append(None)  # Append None for missing values

        print("Finished parsing .fit file. Number of records parsed:", len(data['timestamp']))

        df = pd.DataFrame(data)
        return df
