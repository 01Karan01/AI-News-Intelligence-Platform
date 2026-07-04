import csv
path = 'clustering/clustered_news.csv'
with open(path, 'r', encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader, 1):
        if len(row) != 6:
            print('line', i, 'fields', len(row))
            print(row)
            break
    else:
        print('all rows parsed with 6 fields')
