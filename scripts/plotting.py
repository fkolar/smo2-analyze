# scripts/plotting.py

import pandas as pd  # Ensure pandas is imported
import matplotlib.pyplot as plt
import numpy as np  # Import numpy
from scripts import *

class DataPlotter:
    def __init__(self, df, work_intervals=None):
        self.df = df
        self.work_intervals = work_intervals if work_intervals else []

    def plot_data(self, start_time=None, end_time=None):
        if start_time is None or end_time is None:
            start_time = self.df['elapsed_time'].min()
            end_time = self.df['elapsed_time'].max()

        if start_time == end_time or pd.isna(start_time) or pd.isna(end_time):
            print("Warning: Invalid time range provided. Adjusting to full dataset range.")
            start_time = self.df['elapsed_time'].min()
            end_time = self.df['elapsed_time'].max()

        # Increase the width of the plot for better spacing
        fig, ax1 = plt.subplots(figsize=(12, 6))  # Increased width from 10 to 12

        lines = []

        # Plot Power with a filled background on the primary left Y-axis if SHOW_POWER is True
        if SHOW_POWER:
            ax1.fill_between(self.df['elapsed_time'], 0, self.df[FIELD_MAPPINGS['power']], color=POWER_COLOR, alpha=0.3)
            line_power, = ax1.plot(self.df['elapsed_time'], self.df[FIELD_MAPPINGS['power']], color=POWER_COLOR,
                                   linewidth=POWER_LINEWIDTH, label='Power')
            lines.append(line_power)
            ax1.set_ylabel('Power (Watts)', color=POWER_COLOR)
            ax1.tick_params(axis='y', labelcolor=POWER_COLOR)
            ax1.set_ylim(POWER_RANGE)

            # Make sure SmO2 is plotted on a separate axis
            ax2 = ax1.twinx()
            ax2.spines['left'].set_position(('axes', -0.15))
            line_smo2, = ax2.plot(self.df['elapsed_time'], self.df['smo2_smooth'], color=SMO2_COLOR,
                                  linewidth=SMO2_LINEWIDTH, label='SmO2')
            lines.append(line_smo2)
            ax2.set_ylabel('SmO2 (%)', color=SMO2_COLOR)
            ax2.tick_params(axis='y', labelcolor=SMO2_COLOR)
            ax2.set_ylim(SMO2_RANGE)
        else:
            line_smo2, = ax1.plot(self.df['elapsed_time'], self.df['smo2_smooth'], color=SMO2_COLOR,
                                  linewidth=SMO2_LINEWIDTH, label='SmO2')
            lines.append(line_smo2)
            ax1.set_ylabel('SmO2 (%)', color=SMO2_COLOR)
            ax1.tick_params(axis='y', labelcolor=SMO2_COLOR)
            ax1.set_ylim(SMO2_RANGE)

        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('axes', 1.2))
        if SHOW_HR:
            line_hr, = ax3.plot(self.df['elapsed_time'], self.df['hr_smooth'], color=HR_COLOR, linewidth=HR_LINEWIDTH,
                                label='Heart Rate')
            lines.append(line_hr)
            ax3.set_ylabel('Heart Rate (bpm)', color=HR_COLOR)
            ax3.tick_params(axis='y', labelcolor=HR_COLOR)
            ax3.set_ylim(HR_RANGE)

        ax4 = ax1.twinx()
        ax4.spines['right'].set_position(('axes', 1.35))
        if SHOW_THB:
            line_thb, = ax4.plot(self.df['elapsed_time'], self.df['thb_smooth'], color=THB_COLOR,
                                 linewidth=THB_LINEWIDTH, label='tHb')
            lines.append(line_thb)
            ax4.set_ylabel('tHb (g/dL)', color=THB_COLOR)
            ax4.tick_params(axis='y', labelcolor=THB_COLOR)
            ax4.set_ylim(THB_RANGE)

        if SHOW_GRID:
            ax1.grid(color=GRID_COLOR, alpha=GRID_ALPHA)

        self.plot_smo2_trends(ax2 if SHOW_POWER else ax1)

        plt.title('Power, SmO2, Heart Rate, and tHb over Time')
        plt.xlim(start_time, end_time)

        labels = [line.get_label() for line in lines]
        plt.legend(lines, labels, loc='upper right', fontsize='small')

        fig.tight_layout()
        plt.show()

    def plot_smo2_trends(self, ax):
        if SHOW_SMO2_TREND:
            if not self.work_intervals:
                print("No work intervals defined. Please define work intervals for trend lines.")
                return

            print(f"Plotting trend lines for {len(self.work_intervals)} intervals.")

            for start, end in self.work_intervals:
                delayed_slope_data = self.df[(self.df['elapsed_time'] >= start) & (self.df['elapsed_time'] <= end)]

                if not delayed_slope_data.empty:
                    z = np.polyfit(delayed_slope_data['elapsed_time'], delayed_slope_data['smo2_smooth'], 1)
                    p = np.poly1d(z)
                    ax.plot(delayed_slope_data['elapsed_time'], p(delayed_slope_data['elapsed_time']), color='black',
                            linestyle='-', linewidth=2)  # Thin black line for trend
