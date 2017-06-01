import csv

# Find maximum widths of fields for Postgres

files = [
    'data/organisation.tsv',
    'data/page.tsv',
    'data/attachment.tsv',
    'data/download.tsv',
    'data/history.tsv',
]

sep = '\t'

for file in files:
    reader = csv.DictReader(open(file), delimiter=sep)
    fields = reader.fieldnames
    widths = {}

    for row in reader:
        for field in  fields:
            widths[field] = max(widths.get(field, 0), len(row[field]))
    print(file, widths)
