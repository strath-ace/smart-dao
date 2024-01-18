import matplotlib.pyplot as plt
import matplotlib as matplot
import datetime

def remove_non_unique(arr):
    """
    Removes non-unique values from an array and returns a new array
    with only the unique values.
    """
    unique_arr = []
    for value in arr:
        if value not in unique_arr:
            unique_arr.append(value)
    return unique_arr
events_pre = [
    (datetime.datetime(2023, 2, 6, 1, 17), "Earthquake", "1"),      # 7.8M
    (datetime.datetime(2023, 2, 6, 1, 28), "Earthquake", "2"),      # 6.7M
    (datetime.datetime(2023, 2, 6, 10, 24), "Earthquake", "3"),     # 7.5M
    (datetime.datetime(2023, 2, 6, 1, 38), "Notification", "4" ),    # Adam Map
    (datetime.datetime(2023, 2, 6, 3, 28), "Notification", "5" ),    # Adam Map
    # (datetime.datetime(2023, 2, 7, 19, 46), "Notification", "6" ),    # ECHO Daily
    #(datetime.datetime(2023, 2, 10, 17, 3), "Notification", "7" ),    # ECHO Daily
    # (datetime.datetime(2023, 2, 13, 18, 49), "Notification", "8" ),    # ECHO Daily
    # (datetime.datetime(2023, 2, 17, 12, 17), "Notification", "9" )    # ECHO Daily
    (datetime.datetime(2023, 2, 6, 10, 14), "Copernicus", "7" ),    # Copernicus Act
    # (datetime.datetime(2023, 2, 7, 8, 0), "Copernicus", "7" ),    # Copernicus First Img
    # (datetime.datetime(2023, 2, 8, 16, 0), "Copernicus", "7" ),    # Copernicus First Pub
    #(datetime.datetime(2023, 2, 12, 3, 10), "Copernicus", "7" ),    # Copernicus Last Pub
    (datetime.datetime(2023, 2, 6, 7, 4), "ICSMD", "7" ),    # ICSMD Act
    (datetime.datetime(2023, 2, 6, 1, 26), "Notification", "7" ),    # GTS #1
    (datetime.datetime(2023, 2, 6, 1, 49), "Guages", "7" ),    # Guage #1
    (datetime.datetime(2023, 2, 6, 1, 50), "Guages", "7" ),    # Guage #1
    (datetime.datetime(2023, 2, 6, 2, 10), "Guages", "7" ),    # Guage #1
]


events = []
for val in events_pre:
    events.append((val[0], val[0]+datetime.timedelta(minutes=2), val[1], val[2]))


# Set up the plot
fig, ax = plt.subplots(figsize=(16, 4))

# Add a horizontal line at y=0
ax.axhline(0, color='gray', linewidth=1)

y_marks = remove_non_unique([event[2] for event in events])

# Loop through events and add a horizontal bar for each
for i, event in enumerate(events):
    start = event[0]
    end = event[1]
    row = event[2]
    for i in range(len(y_marks)):
        if row == y_marks[i]:
            pos = i
    label = event[3]
    duration = end - start
    ax.barh(pos, duration, left=start, height=0.9, align='center', color='black')
    ax.text(start + duration / 2, pos, label, ha='center', va='center', color='red')
    

# Set the y-axis ticks to be the event labels

ax.set_yticks(range(len(y_marks)))
ax.set_yticklabels(y_marks)

# Set the x-axis limits to be the min and max dates
min_date = min(event[0] for event in events)
max_date = max(event[1] for event in events)
ax.set_xlim(min_date, max_date)

# Set the x-axis tick format to be month/year
date_format = matplot.dates.DateFormatter('%Hh %dth')
ax.xaxis.set_major_formatter(date_format)

# Add a title and labels to the plot
ax.set_title("Timeline")
ax.set_xlabel("Date")
ax.set_ylabel("Event")

# Show the plot
plt.savefig("output.png", transparent=True)