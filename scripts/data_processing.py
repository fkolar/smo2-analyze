# scripts/data_processing.py

import pandas as pd
from scripts import SMOOTHING_WINDOW, MIN_PERIODS, FIELD_MAPPINGS

class DataProcessor:
    def __init__(self, df):
        self.df = df

    def calculate_elapsed_time(self):
        timestamp_field = FIELD_MAPPINGS['timestamp']
        self.df[timestamp_field] = pd.to_datetime(self.df[timestamp_field], errors='coerce')
        self.df.dropna(subset=[timestamp_field], inplace=True)
        self.df['elapsed_time'] = (self.df[timestamp_field] - self.df[timestamp_field].min()).dt.total_seconds() / 60

    def smooth_data(self):
        print("Available columns in DataFrame:", self.df.columns)
        required_fields = ['smo2', 'hr', 'thb']
        for field in required_fields:
            mapped_field = FIELD_MAPPINGS[field]
            if mapped_field in self.df.columns:
                self.df[f'{field}_smooth'] = self.df[mapped_field].rolling(window=SMOOTHING_WINDOW,
                                                                           min_periods=MIN_PERIODS).mean()
            else:
                print(f"Error: The required field '{mapped_field}' is not present in the DataFrame.")
                raise ValueError(f"The required field '{mapped_field}' is not present in the DataFrame.")

    def identify_delayed_intervals(self):
        """
        Identify work intervals based on a fixed pattern and define sub-intervals
        for trend line analysis (last 4 minutes of each 5-minute work interval).
        """
        work_intervals = []
        min_time = self.df['elapsed_time'].min()
        max_time = self.df['elapsed_time'].max()

        # Define work intervals: each 5 minutes of work, followed by 1 minute break
        start = min_time
        interval_count = 1

        while start + 5 <= max_time:
            work_start = start
            work_end = start + 5

            # Define the sub-interval for the last 4 minutes of the work interval
            trend_start = work_start + 1  # Start at the 2nd minute of the work interval
            trend_end = work_end  # End at the 5th minute

            print(f"Interval #{interval_count} starts from {work_start:.2f} min to {work_end:.2f} min.")
            print(f"Trend line for interval #{interval_count} will be analyzed from {trend_start:.2f} min to {trend_end:.2f} min.")

            work_intervals.append((trend_start, trend_end))

            # Move to the next interval after a 1-minute break
            start += 6  # 5 minutes of work + 1 minute of break
            interval_count += 1

        print(f"Total work intervals detected: {len(work_intervals)}")
        return work_intervals

    def process(self):
        self.calculate_elapsed_time()
        self.smooth_data()
        delayed_intervals = self.identify_delayed_intervals()
        return self.df, delayed_intervals
