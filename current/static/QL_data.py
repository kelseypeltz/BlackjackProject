import csv

with open('QL_data.txt', mode='r') as file:
    lines = file.readlines()

data = []
i = 0
while i < len(lines):
    if lines[i].strip() == '':
        i += 1
        continue
    iterations = int(lines[i].split(':')[1].strip())
    win = float(lines[i+1].split(':')[1].strip().replace('%', ''))/100
    draw = float(lines[i+2].split(':')[1].strip().replace('%', ''))/100
    lose = float(lines[i+3].split(':')[1].strip().replace('%', ''))/100
    data.append([iterations, win, draw, lose])
    i += 4

with open('QL_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Iterations', 'Win', 'Draw', 'Lose'])
    for row in data:
        writer.writerow(row)
