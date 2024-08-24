# scripts/data_processing.py

import pandas as pd
import numpy as np
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

    def calculate_slope_for_intervals(self, intervals):
        """
        Calculate and print the slope of SmO2 for each interval.
        """
        print("Calculating slopes for intervals...")
        slopes = []
        for i, (start, end) in enumerate(intervals):
            interval_data = self.df[(self.df['elapsed_time'] >= start) & (self.df['elapsed_time'] <= end)]
            if not interval_data.empty:
                x = interval_data['elapsed_time']
                y = interval_data['smo2_smooth']
                # Calculate the slope using numpy polyfit
                slope, intercept = np.polyfit(x, y, 1)
                slopes.append(slope)
                print(f"Slope for Interval #{i + 1} ({start:.2f} min to {end:.2f} min): {slope:.4f}")
            else:
                print(f"Interval #{i + 1} ({start:.2f} min to {end:.2f} min) has no data.")

        print("Completed slope calculation.")
        return slopes

    def identify_delayed_intervals(self):
        """
        Identify work intervals based on a fixed pattern and define sub-intervals
        for trend line analysis (last 4 minutes of each 5-minute work interval).
        """
        work_intervals = []
        min_time = self.df['elapsed_time'].min()
        max_time = self.df['elapsed_time'].max()

        start = min_time
        interval_count = 1

        while start + 5 <= max_time:
            work_start = start
            work_end = start + 5

            trend_start = work_start + 1  # Start at the 2nd minute of the work interval
            trend_end = work_end  # End at the 5th minute

            print(f"Interval #{interval_count} starts from {work_start:.2f} min to {work_end:.2f} min.")
            print(f"Trend line for interval #{interval_count} will be analyzed from {trend_start:.2f} min to {trend_end:.2f} min.")

            work_intervals.append((trend_start, trend_end))

            start += 6  # Move to the next interval after a 1-minute break
            interval_count += 1

        print(f"Total work intervals detected: {len(work_intervals)}")
        return work_intervals

    def process(self):
        self.calculate_elapsed_time()
        self.smooth_data()
        delayed_intervals = self.identify_delayed_intervals()
        slopes = self.calculate_slope_for_intervals(delayed_intervals)  # Calculate slopes for each interval
        return self.df, delayed_intervals, slopes
