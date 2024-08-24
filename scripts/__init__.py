# scripts/__init__.py

# Configuration settings for visibility
SHOW_POWER = True
SHOW_SMO2 = True
SHOW_HR = True
SHOW_THB = True
SHOW_SMO2_TREND = True  # For 5-minute intervals, skipping 1st minute
SHOW_OVERALL_SMO2_TREND = False
SHOW_REST_SMO2_PEAKS_TREND = False


# New configuration setting to toggle chart type
SHOW_SMO2_SLOPE_VS_POWER = False  # Set to True to show SmO2 slope vs. Power chart



# Configuration settings for zooming
ZOOM_ENABLED = False  # Default to False; set to True to enable zooming

# Configuration settings for grid lines
SHOW_GRID = True  # Default to True; set to False to disable grid lines
GRID_COLOR = 'grey'  # Color of the grid lines
GRID_ALPHA = 0.5  # Transparency of the grid lines (0 to 1)

# Configuration settings for ranges
POWER_RANGE = [0, 250]
SMO2_RANGE = [20, 90]  # Adjust based on actual data
HR_RANGE = [0, 188]
THB_RANGE = [11.8, 12.7]

# Configuration settings for smoothing
SMOOTHING_WINDOW = 7  # Number of data points to include in the rolling mean
MIN_PERIODS = 1  # Minimum number of observations in the window required to have a value

# Configuration settings for plot aesthetics
# Colors
POWER_COLOR = 'lightgrey'
SMO2_COLOR = 'green'
HR_COLOR = 'red'
THB_COLOR = 'brown'
SMO2_TREND_COLOR = 'black'
OVERALL_SMO2_TREND_COLOR = 'blue'
REST_SMO2_PEAKS_TREND_COLOR = 'purple'

# Line thicknesses
POWER_LINEWIDTH = 1
SMO2_LINEWIDTH = 2
HR_LINEWIDTH = 1
THB_LINEWIDTH = 1
SMO2_TREND_LINEWIDTH = 1
OVERALL_SMO2_TREND_LINEWIDTH = 1
REST_SMO2_PEAKS_TREND_LINEWIDTH = 2

# Line styles
POWER_LINESTYLE = '-'
SMO2_LINESTYLE = '-'
HR_LINESTYLE = '-'
THB_LINESTYLE = '-'
SMO2_TREND_LINESTYLE = '--'
OVERALL_SMO2_TREND_LINESTYLE = '-'
REST_SMO2_PEAKS_TREND_LINESTYLE = '-'

# Corrected field mappings for different .fit files
FIELD_MAPPINGS = {
    'timestamp': 'timestamp',  # Actual timestamp field name in your .fit file
    'power': 'power',          # Actual power field name in your .fit file
    'smo2': 'smo2',            # Correct SmO2 field name in your .fit file
    'hr': 'heart_rate',                # Correct heart rate field name in your .fit file
    'thb': 'thb'               # Correct tHb field name in your .fit file
}
