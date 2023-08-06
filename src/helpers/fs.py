import json
import os
from datetime import datetime

from src.helpers.parsers import clean_list


def export_csv(json_list, n):
    # Setup Local Variables
    filename = datetime.now()
    filename = filename.strftime("%Y-%m-%d")

    # Create the header if the file does not exist, or is empty
    output_dir = f"output/{filename}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(f"{output_dir}/{n}.csv", "a+") as f:
            lines = f.read().splitlines()

            if len(lines) == 0 and len(json_list) > 0:
                try:
                    f.write(",".join(clean_list(json_list[0].keys())) + "\n")
                except:
                    pass

            # Append the data to the csv file
            for stock in json_list:
                f.write(",".join(clean_list((json.loads(stock) if type(stock) != dict else stock).values())) + "\n")

            return True
    except Exception as e:
        raise e
