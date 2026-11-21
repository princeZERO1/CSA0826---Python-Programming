"""The hostel office's ORIGINAL script (only the path changed so it can run here)."""
f = open("mess_oct.txt")
data = f.read()
total = 0
report = ""
for line in data.split("\n"):
    try:
        parts = line.split(",")
        total = total + int(parts[2])
        report = report + parts[1] + " " + parts[2] + "\n"
    except:
        pass
print(report)
print("Total", total)
