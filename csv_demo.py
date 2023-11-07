import csv


def write_to_csv(data, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ["Directory", "File", "PackageName", "ImportedPackage", "FunctionCall"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            writer.writerow({
                "Directory": row.get("Directory", ""),
                "File": row.get("File", ""),
                "PackageName": row.get("PackageName", ""),
                "ImportedPackage": row.get("ImportedPackage", ""),
                "FunctionCall": row.get("FunctionCall", ""),
            })


if __name__ == '__main__':
    # 示例数据
    data = [
        {
            "Directory": "/path/to/directory1",
            "File": "file1",
            "PackageName": "package1",
            "ImportedPackage": "package2",
            "FunctionCall": "function1",
        },
        {
            "Directory": "",
            "File": "",
            "PackageName": "",
            "ImportedPackage": "",
            "FunctionCall": "function2",
        },
        {
            "Directory": "/path/to/directory2",
            "File": "file2",
            "PackageName": "package2",
            "ImportedPackage": "package3",
            "FunctionCall": "function3",
        },
        {
            "Directory": "",
            "File": "",
            "PackageName": "",
            "ImportedPackage": "",
            "FunctionCall": "function4",
        },
    ]

    csv_filename = "output.csv"
    write_to_csv(data, csv_filename)
