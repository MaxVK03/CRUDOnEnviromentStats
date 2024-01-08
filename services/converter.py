import io
import csv

"""
Helper function that converts the standard JSON result into CSV values. 
This function is called when the user requests for CSV. 
"""
def csvSender(result):
    if not result:
        return ""

    data_dicts = [item.to_dict() for item in result] if hasattr(result[0], 'to_dict') else [vars(item) for item in
                                                                                            result]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data_dicts[0].keys())
    writer.writeheader()

    for row in data_dicts:
        writer.writerow(row)

    csv_string = output.getvalue()
    output.close()
    return csv_string
