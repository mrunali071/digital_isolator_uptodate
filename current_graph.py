import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
data = pd.read_csv(r"C:\testresults\18012015421H\supply_current_device_18012015421H.csv")

# Data cleaning and preprocessing
data = data.dropna(subset=['sample_number', 'temperature_deg', 'frequency', 'vcc1_V', 'ICC1_A', 'ICC2_A'])
data['sample_number'] = data['sample_number'].astype(int)
data['temperature_deg'] = data['temperature_deg'].astype(int)
data['vcc1_V'] = data['vcc1_V'].astype(float)

# Separate DC and AC data
data_dc = data[data['frequency'].str.contains('DC', na=False)]
data_ac = data[~data['frequency'].str.contains('DC', na=False)]

# Create a copy of AC data and extract numerical frequency
data_ac = data_ac.copy()
data_ac['frequency'] = data_ac['frequency'].str.extract(r'(\d+\.?\d*)').astype(float)

# Function to plot DC data for a specific ICC
def plot_dc_data(data_dc, current_col, current_label):
    unique_temperatures = data_dc['temperature_deg'].unique()
    
    for temp in unique_temperatures:
        subset = data_dc[data_dc['temperature_deg'] == temp]
        samples = subset['sample_number'].unique()

        # Bar positions and width
        x = np.arange(len(samples))
        bar_width = 0.25

        # Separate data for different Vcc1 levels
        vcc5 = subset[subset['vcc1_V'] == 5.0]
        vcc3_3 = subset[subset['vcc1_V'] == 3.3]
        vcc2_5 = subset[subset['vcc1_V'] == 2.5]

        # Plotting bars
        plt.figure(figsize=(14, 8))
        plt.bar(x - bar_width, vcc5[current_col], bar_width, label='Vcc1=5V, Vcc2=5V', color='red')
        plt.bar(x, vcc3_3[current_col], bar_width, label='Vcc1=3.3V, Vcc2=3.3V', color='gray')
        plt.bar(x + bar_width, vcc2_5[current_col], bar_width, label='Vcc1=2.5V, Vcc2=2.5V', color='blue')

        # Adding labels and titles
        plt.title(f'{current_label} DC Current at Temperature {temp}°C')
        plt.xlabel('Samples')
        plt.ylabel('Current (mA)')
        plt.xticks(x, samples)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Show the graph
        plt.show()

# Function to plot AC data for a specific ICC
def plot_ac_data(data_ac, current_col, current_label):
    unique_temperatures = data_ac['temperature_deg'].unique()
    unique_frequencies = data_ac['frequency'].unique()
    
    for temp in unique_temperatures:
        for freq in unique_frequencies:
            subset = data_ac[(data_ac['temperature_deg'] == temp) & (data_ac['frequency'] == freq)]
            if subset.empty:
                continue

            samples = subset['sample_number'].unique()

            # Bar positions and width
            x = np.arange(len(samples))
            bar_width = 0.25

            # Separate data for different Vcc1 levels
            vcc5 = subset[subset['vcc1_V'] == 5.0]
            vcc3_3 = subset[subset['vcc1_V'] == 3.3]
            vcc2_5 = subset[subset['vcc1_V'] == 2.5]

            # Plotting bars
            plt.figure(figsize=(14, 8))
            plt.bar(x - bar_width, vcc5[current_col], bar_width, label='Vcc1=5V, Vcc2=5V', color='red')
            plt.bar(x, vcc3_3[current_col], bar_width, label='Vcc1=3.3V, Vcc2=3.3V', color='gray')
            plt.bar(x + bar_width, vcc2_5[current_col], bar_width, label='Vcc1=2.5V, Vcc2=2.5V', color='blue')

            # Adding labels and titles
            plt.title(f'{current_label} AC Current at Temperature {temp}°C and Frequency {freq} MHz')
            plt.xlabel('Samples')
            plt.ylabel('Current (mA)')
            plt.xticks(x, samples)
            plt.legend()
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Show the graph
            plt.show()

# Generate DC graphs for ICC1 and ICC2
plot_dc_data(data_dc, 'ICC1_A', 'ICC1')
plot_dc_data(data_dc, 'ICC2_A', 'ICC2')

# Generate AC graphs for ICC1 and ICC2
plot_ac_data(data_ac, 'ICC1_A', 'ICC1')
plot_ac_data(data_ac, 'ICC2_A', 'ICC2')
