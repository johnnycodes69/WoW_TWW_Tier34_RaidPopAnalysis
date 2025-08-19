import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import shutil

# setup paths
BASE_DIR = Path(__file__).resolve().parent     # captures where the script is running
DATA_DIR = BASE_DIR / "Manaforge_Omega_stats"  # subdirectory for CSV files
ARCHIVE_DIR = DATA_DIR / "archive"             # the archive

# create the archive just in case...
ARCHIVE_DIR.mkdir(exist_ok=True)

data_file = DATA_DIR / "manaforge_omega_week1.csv" # historical data
new_file = DATA_DIR / "manaforge_omega_week2.csv" # new data

# load data unless no historical data then just go
if data_file.exists():
    hist = pd.read_csv(data_file)
else:
    hist = pd.DataFrame(columns=["Week","Spec","Population"])

# load new week's data
new = pd.read_csv(new_file)  # must have Spec and Population columns
week_stamp = pd.Timestamp.today().strftime("%Y-%m-%d")
new["Week"] = week_stamp

# append and save the updated hist data
hist = pd.concat([hist, new], ignore_index=True)
hist.to_csv(data_file, index=False)

# generate chart last week
latest = hist[hist["Week"] == new["Week"].iloc[0]]

# archive the processed weekly file
archive_file = ARCHIVE_DIR / f"weekly_{week_stamp}.csv"
shutil.move(str(new_file), archive_file)    # moves and renames file

latest = hist[hist["Week"] == week_stamp]

# alphabetical axis (axies?)
latest = latest.sort_values("Spec")

# sort the bars in the chart by value
sorted_by_value = latest.sort_values("Population", ascending=False)

plt.figure(figsize=(8,5))
plt.barh(sorted_by_value["Spec"], sorted_by_value["Population"])
plt.title(f"Weekly Values ({week_stamp})")
plt.xlabel("Population")
plt.ylabel("Spec (Alphabetical)")
plt.tight_layout()

# save the charts
chart_file = DATA_DIR / f"chart_{week_stamp}.png"
plt.savefig(chart_file)
plt.show()

print(f"Historical data updated: {data_file}")
print(f"Chart saved: {chart_file}")
print(f"Weekly file archived: {archive_file}")