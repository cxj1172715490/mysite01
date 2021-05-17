import csv

with open('test_csv.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['a', 'b', 'c'])  # 执行一次导入一条
    writer.writerow(['d', 'e'])
