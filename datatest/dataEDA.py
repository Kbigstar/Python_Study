import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the CSV file
file_path = 'ener.csv'  # 파일 경로를 지정해주세요
data = pd.read_csv(file_path)

# Ensure ENER_DT is in 'YYYYMM' format as a string
data['ENER_DT'] = data['ENER_DT'].astype(str)

# Convert ENER_DT to datetime for time series analysis
data['ENER_DT'] = pd.to_datetime(data['ENER_DT'], format='%Y%m')

# Filter data to include only COMPLEXCODE, ENER_DT, and ELEC_USAGE
filtered_data = data[['COMPLEXCODE', 'ENER_DT', 'ELEC_USAGE']].copy()

# Pivot the data to ensure all dates are included for each complex code
pivot_table = filtered_data.pivot_table(index='ENER_DT', columns='COMPLEXCODE', values='ELEC_USAGE', aggfunc='sum')

# Create a date range from 201401 to 202312
full_date_range = pd.date_range(start='2014-01-01', end='2023-12-01', freq='MS')

# Reindex the pivot table to include all dates in the full date range and fill missing values with 0
pivot_table = pivot_table.reindex(full_date_range, fill_value=0)

# Sum ELEC_USAGE across all complex codes for each date
monthly_data = pivot_table.sum(axis=1)

# Plotting the time series to identify seasonality
plt.figure(figsize=(36, 16))  # 그래프 크기 조정
plt.plot(monthly_data.index, monthly_data, marker='o', linestyle='-')
plt.title('Monthly ELEC_USAGE Over Time')
plt.xlabel('Date')
plt.ylabel('ELEC_USAGE')
plt.grid(True)

# Setting x-axis major locator and formatter
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # 모든 연월을 표시
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))

# Set the x-axis limits to match the data range
ax.set_xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2023-12-31'))

plt.xticks(rotation=90, ha='center')
plt.show()
