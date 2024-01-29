import fitz
import json
from tqdm import tqdm
import pandas as pd
from pathlib import Path

def overlap(bbox, gt_bbox):
    x_overlap = min(bbox[2], gt_bbox[2]) - max(bbox[0], gt_bbox[0])
    y_overlap = min(bbox[3], gt_bbox[3]) - max(bbox[1], gt_bbox[1])
    if x_overlap > 0 and y_overlap > 0:
        overlap_area = x_overlap*y_overlap
        bbox_area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])
        if overlap_area/bbox_area > 0.6:
            return True
    return False       

def get_label(bbox, gt_row):
    label = "other"
    for col in gt_row.columns:
        if "filename" not in col:
            for row in gt_row[col]:
                # print(f"Row: {row}")
                for gt_box in eval(row):
                    gt_bbox = gt_box[:4]
                    if overlap(bbox, gt_bbox):
                        label = col
                        return label
    return label

def get_gt_dict(words_list, gt_row):
    # print("getting gt dict")
    n_words = len(words_list)
    n_sub_lists = n_words//200 if n_words%200==0 else n_words//200+1
    gt_dict_list = list()
    for i in range(n_sub_lists):
        sub_list = words_list[200*i:200*(i+1)] if i <n_sub_lists-1 else words_list[200*i:]
        gt_dict = {"form": list()}
        for id, word in enumerate(sub_list):
            word_bbox = [int(w) for w in word[:4]]
            label = get_label(word_bbox, gt_row)
            temp_dict = {"box": word_bbox, "text": word[4], "label": label, "linking": [], "id": id}
            temp_dict["words"] = [{"box": word_bbox, "text": w} for w in word[4].split()]
            gt_dict["form"].append(temp_dict)
        gt_dict_list.append(gt_dict)
    return gt_dict_list


def get_pdf_text_and_image(pdf_path):
    with fitz.open(pdf_path) as doc:
        page = doc[0]
        pdf_image = page.get_pixmap()
        words_list = page.get_text("words", sort=True)
    return words_list, pdf_image

def create_dataset(pdf_path, gt_row, split):
    # print("Creating dataset")
    words_list, pdf_image = get_pdf_text_and_image(pdf_path)
    gt_dict_list = get_gt_dict(words_list, gt_row)
    return gt_dict_list, pdf_image

if __name__ == "__main__":
    pdf_dir = Path("dataset/PDFs")
    gt_excel_path = "dataset/gt_100.xlsx"
    output_dir = Path("dataset")

    train_images_dir = output_dir.joinpath("training_data/images")
    train_images_dir.mkdir(parents=True, exist_ok=True)
    train_annotation_dir = output_dir.joinpath("training_data/annotations")
    train_annotation_dir.mkdir(parents=True, exist_ok=True)
    test_images_dir = output_dir.joinpath("testing_data/images")
    test_images_dir.mkdir(parents=True, exist_ok=True)
    test_annotation_dir = output_dir.joinpath("testing_data/annotations")
    test_annotation_dir.mkdir(parents=True, exist_ok=True)

    gt_df = pd.read_excel(gt_excel_path)
    pdf_paths_list = pdf_dir.glob("*.pdf")
    n = 100
    i = 0
    for pdf_path in tqdm(pdf_paths_list):
        # print(i)
        if i < 0.7*n:
            split = "train"
        else:
            split = "test"
        gt_row = gt_df[gt_df["filename"]==f"PDFs/{pdf_path.name}"]
        gt_dict_list, pdf_image = create_dataset(pdf_path, gt_row, split)
        for idx, gt_dict in enumerate(gt_dict_list):
            if split == "train":            
                with open(train_annotation_dir.joinpath(f"{pdf_path.stem}_{idx}.json"), "w") as outfile: 
                    json.dump(gt_dict, outfile, indent = 2)
                pdf_image.save(train_images_dir.joinpath(f"{pdf_path.stem}_{idx}.png"))
            else:
                with open(test_annotation_dir.joinpath(f"{pdf_path.stem}_{idx}.json"), "w") as outfile: 
                    json.dump(gt_dict, outfile, indent = 2)
                pdf_image.save(test_images_dir.joinpath(f"{pdf_path.stem}_{idx}.png"))
        i += 1
