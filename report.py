import sys
import open as op

file_path = sys.argv[1]

print(file_path)

ws = op.data(file_path).active

for each in ws.rows:
    print(each)