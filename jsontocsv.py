import argparse
import json
import csv
import sys
import pandas as pd

def flatten(obj, parent_key='', sep='.'):
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten(v, new_key, sep=sep))
    elif isinstance(obj, list):
        # convert lists to JSON string to avoid exploding rows/columns
        items[parent_key] = json.dumps(obj, ensure_ascii=False)
    else:
        items[parent_key] = obj
    return items

def json_to_rows(data):
    # If top-level is dict of equal-length lists -> treat as columns
    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        lengths = {len(v) for v in data.values()}
        if len(lengths) == 1:
            # convert columns to list of row dicts
            keys = list(data.keys())
            rows = []
            for i in range(len(next(iter(data.values())))):
                row = {k: data[k][i] for k in keys}
                rows.append(row)
            return rows
    # If top-level is a list of objects
    if isinstance(data, list):
        rows = []
        for item in data:
            if isinstance(item, dict):
                rows.append(flatten(item))
            else:
                # non-dict items -> store as a single column "value"
                rows.append({'value': item})
        return rows
    # Single object -> one row
    if isinstance(data, dict):
        return [flatten(data)]
    # Scalar -> one-row single-column
    return [{'value': data}]

def write_csv(rows, out_path):
    if not rows:
        # empty output
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            f.write('')
        return
    # Collect all fieldnames (union of keys)
    fieldnames = []
    seen = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for r in rows:
            writer.writerow({k: ('' if v is None else v) for k, v in r.items()})

def main():
    p = argparse.ArgumentParser(description="Convert JSON to CSV")
    p.add_argument('input', help='Input JSON file')
    p.add_argument('output', help='Output CSV file')
    args = p.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to read/parse JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Try pandas for nested normalization if available and if data is list/dict
    try:
        
        if isinstance(data, (list, dict)):
            # Use json_normalize for better handling of nested lists/dicts
            try:
                df = pd.json_normalize(data)
                df.to_csv(args.output, index=False, encoding='utf-8')
                return
            except Exception:
                pass
    except Exception:
        pass

    rows = json_to_rows(data)
    write_csv(rows, args.output)

if __name__ == '__main__':
    main()