import pandas as pd
import matplotlib.pyplot as plt

# Load the exported CSV file
rsi_data = pd.read_csv('/tmp/ethusdt_5m_rsi.csv')

# Convert the calculated_at column to datetime
rsi_data['calculated_at'] = pd.to_datetime(rsi_data['calculated_at'])

# Plot RSI values over time
plt.figure(figsize=(12, 6))  # Optional: Adjust figure size
plt.plot(rsi_data['calculated_at'], rsi_data['indicator_value'], label='RSI')
plt.title('ETHUSDT RSI (5m Interval)')
plt.xlabel('Time')
plt.ylabel('RSI')
plt.axhline(70, color='red', linestyle='--', label='Overbought')
plt.axhline(30, color='green', linestyle='--', label='Oversold')
plt.legend()

# Save the plot as an image file
plt.savefig('/tmp/ethusdt_rsi_5m.png')

# Notify the user where the plot is saved
print("RSI plot saved as /tmp/ethusdt_rsi_5m.png")

