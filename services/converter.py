import io
import csv


def csvSender(result):
    if not result:
        return ""

    if isinstance(result[0], dict):
        data_dicts = result
    else:
        data_dicts = [item.to_dict() if hasattr(item, 'to_dict') else vars(item) for item in result]

    data_dicts = [{key: value for key, value in row.items() if not key.startswith('_sa_instance_state')}
                  for row in data_dicts]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data_dicts[0].keys())
    writer.writeheader()

    for row in data_dicts:
        writer.writerow(row)

    return output.getvalue()
