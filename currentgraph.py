import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file (update the path if needed)
data = pd.read_csv(r"C:\testresults\18012015421H\supply_current_device_18012015421H.csv")

# Display the first few rows to check the loaded data
print("Original Data preview:")
print(data.head())

# Define column names (adjust based on the actual column names in your CSV)
sample_column = 'sample_number'  # Adjust based on actual name
frequency_column = 'frequency'
vcc1_column = 'vcc1'
vcc2_column = 'vcc2'
icc1_column = 'ICC1'
icc2_column = 'ICC2'
temperature_column = 'temperature'  # Adjust based on actual name if needed

# Filter out rows with missing sample numbers
data = data.dropna(subset=[sample_column])

# Convert sample column to integer for indexing
data[sample_column] = data[sample_column].astype(int)

# Filter for 'DC' frequency rows
data_dc = data[data[frequency_column] == 'DC']
print("\nFiltered DC data preview:")
print(data_dc[[sample_column, frequency_column, vcc1_column, vcc2_column, icc1_column, icc2_column, temperature_column]].head())

# Define VCC levels and offsets
vcc_levels = [(5, 5), (3.3, 3.3), (2.5, 2.5)]
offsets = np.array([-0.2, 0, 0.2])  # Adjust bar positions
colors = ['#D62728', '#7F7F7F', '#1F77B4']  # Red, Gray, Blue

# Limits for max and typ reference lines
max_limit = 25
typ_limit = 10

# Define temperatures to plot
temperatures = [-40, 25, 125]

# Plot each ICC1 and ICC2 graph at each temperature
for icc_column in [icc1_column, icc2_column]:
    for temp in temperatures:
        plt.figure(figsize=(14, 7))
        plt.title(f'{icc_column} at {temp}°C for DC Supply Current')

        # Filter data for the specific temperature
        temp_data = data_dc[data_dc[temperature_column] == temp]

        # Loop through each VCC level and filter data to plot
        for i, (vcc1, vcc2) in enumerate(vcc_levels):
            subset = temp_data[(temp_data[vcc1_column] == vcc1) & (temp_data[vcc2_column] == vcc2)]
            
            # Print each subset to confirm data is being filtered correctly
            print(f"\nSubset for {icc_column} at {temp}°C with Vcc1={vcc1}V and Vcc2={vcc2}V:")
            print(subset[[sample_column, icc_column]].head())

            # If subset is empty, skip plotting for this VCC level
            if subset.empty:
                print(f"No data available for {icc_column} at {temp}°C with Vcc1={vcc1}V and Vcc2={vcc2}V.")
                continue

            # Plot bars with offsets for each VCC level
            bars = plt.bar(subset[sample_column] + offsets[i], subset[icc_column], 
                           width=0.2, label=f'Vcc1={vcc1}V, Vcc2={vcc2}V', color=colors[i])
            
            # Add annotations on top of each bar
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval, 2),
                         ha='center', va='bottom', fontsize=8)

        # Add max and typ reference lines
        plt.axhline(y=max_limit, color='red', linestyle='--', linewidth=1, label='max. limit')
        plt.axhline(y=typ_limit, color='orange', linestyle='--', linewidth=1, label='typ. limit')

        # Labels and legend
        plt.xlabel('Samples')
        plt.ylabel(f'{icc_column} Current (mA)')
        plt.xticks(temp_data[sample_column].unique())  # Ensure proper sample labels
        plt.legend()

        # Show plot for each temperature and ICC value
        plt.show()
