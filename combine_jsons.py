"""Takes multiple jsons with same keys and combines into a single json.
The values for a particular key comes from the json where the values for
that key are non-empty."""
import json
from pathlib import Path


input_json_dir = Path("outputs")
output_json_dir = Path("outputs_combined")
output_json_dir.mkdir(parents=True, exist_ok=True)

def create_comb_json_and_save(files_doing):
    out_path = output_json_dir.joinpath(f"{'_'.join(files_doing[0].name.split('_')[:-1])}.json")
    with open(files_doing[0], "r") as f:
        out_json = json.load(f)
        if len(files_doing) > 1:
            for file in files_doing[1:]:
                with open(file, "r") as f:
                    temp_json = json.load(f)
                for ele_dict in out_json["output"]:
                    class_name = ele_dict["class"]
                    temp_ele_dict = [temp_dict for temp_dict in temp_json["output"] if temp_dict["class"]==class_name][0]
                    ele_dict["gt"].extend(temp_ele_dict["gt"])
                    ele_dict["pred"].extend(temp_ele_dict["pred"])
    with open(out_path, "w") as f:
        json.dump(out_json, f, indent=2)

files_done = list()
input_files_list = list(input_json_dir.glob("*.json"))
for file in input_files_list:
    filename = file.name
    if filename not in files_done:
        files_doing = [file for file in input_files_list if "_".join(file.name.split("_")[:-1]) == "_".join(filename.split("_")[:-1])]
        files_done.extend([file.name for file in files_doing])
        create_comb_json_and_save(files_doing)

        