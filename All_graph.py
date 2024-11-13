import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv(r'C:\testresults\18012015421H\timing_characteristics_device_18012015421H.csv')

# Drop rows where sample_number is NaN
df = df.dropna(subset=['sample_number'])

# Define a function to plot the data
def plot_sample_data(sample_data, sample_number, time_type='t_r'):
    # Create a new figure for each plot
    plt.figure(figsize=(10, 6))
    
    # Get unique channels and vcc values for this sample
    channels = sample_data['channel'].unique()
    vcc_values = sample_data['vcc1'].unique()  # Assuming vcc1 is the correct column for vcc

    for channel in channels:
        for vcc in vcc_values:
            # Filter data for the specific channel and vcc
            filtered_data = sample_data[(sample_data['channel'] == channel) & (sample_data['vcc1'] == vcc)]
            # Plot time (t_r, t_f, tPLH, tPHL) against temperature for this channel and vcc
            plt.plot(filtered_data['temperature'], filtered_data[time_type], 
                     label=f'Channel {channel}, Vcc {vcc}V', marker='o', linestyle='-')

    # Adding titles and labels based on time type
    if time_type == 't_r':
        plt.title(f'Rise Time vs Temperature for Sample {sample_number}')
        plt.ylabel('Rise Time_tr(ns)')
    elif time_type == 't_f':
        plt.title(f'Fall Time vs Temperature for Sample {sample_number}')
        plt.ylabel('Fall Time_tf(ns)')
    elif time_type == 'tPLH':
        plt.title(f'tPLH vs Temperature for Sample {sample_number}')
        plt.ylabel('tPLH (s)')
    elif time_type == 'tPHL':
        plt.title(f'tPHL vs Temperature for Sample {sample_number}')
        plt.ylabel('tPHL (s)')
    
    plt.xlabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)

# Get unique sample numbers from the DataFrame, excluding NaN values
unique_samples = df['sample_number'].dropna().unique()

# Plot graphs for rise time (t_r), fall time (t_f), tPLH, and tPHL for each sample
for sample in unique_samples:
    sample_data = df[df['sample_number'] == sample]
    
    # Plot rise time (t_r)
    plot_sample_data(sample_data, sample, time_type='t_r')
    # Plot fall time (t_f)
    plot_sample_data(sample_data, sample, time_type='t_f')
    # Plot tPLH
    plot_sample_data(sample_data, sample, time_type='tPLH')
    # Plot tPHL
    plot_sample_data(sample_data, sample, time_type='tPHL')

# Show all plots simultaneously
plt.show()
