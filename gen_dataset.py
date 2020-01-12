import glob
import os
import xml.etree.ElementTree as ET
import sys
import numpy as np


def main(input_folder):

    if not os.path.exists(input_folder):
        print("Dataset not found: " + input_folder)

    DATASET_FOLDER = os.path.join(input_folder, "images/")
    XML_FOLDER = os.path.join(input_folder, "annotations/xmls/")
    TRAIN_OUTPUT_FILE = os.path.join(input_folder, "train.txt")
    TEST_OUTPUT_FILE = os.path.join(input_folder, "test.txt")
    CLASS_OUTPUT_FILE = os.path.join(input_folder, "class.txt")
    SPLIT_RATIO = 0.8

    class_names = {}
    k = 0
    output = []
    xml_files = glob.glob("{}/*xml".format(XML_FOLDER))
    for i, xml_file in enumerate(xml_files):
        tree = ET.parse(xml_file)

        path = os.path.join(DATASET_FOLDER, tree.findtext("./filename"))

        height = int(tree.findtext("./size/height"))
        width = int(tree.findtext("./size/width"))
        xmin = int(tree.findtext("./object/bndbox/xmin"))
        ymin = int(tree.findtext("./object/bndbox/ymin"))
        xmax = int(tree.findtext("./object/bndbox/xmax"))
        ymax = int(tree.findtext("./object/bndbox/ymax"))

        basename = os.path.basename(path)
        basename = os.path.splitext(basename)[0]
        class_name = basename[:basename.rfind("_")].lower()
        if class_name not in class_names:
            class_names[class_name] = k
            k += 1

        output.append((path, height, width, xmin, ymin, xmax,
                       ymax, class_name, class_names[class_name]))

    # preserve percentage of samples for each class ("stratified")
    output.sort(key=lambda tup: tup[-1])

    lengths = []
    i = 0
    last = 0
    for j, row in enumerate(output):
        if last == row[-1]:
            i += 1
        else:
            print("class {}: {} images".format(output[j-1][-2], i))
            lengths.append(i)
            i = 1
            last += 1

    print("class {}: {} images".format(output[j-1][-2], i))
    lengths.append(i)

    with open(CLASS_OUTPUT_FILE, "w") as classes:
        for class_name in class_names:
            classes.writelines(class_name + '\n')

    with open(TRAIN_OUTPUT_FILE, "w") as train, open(TEST_OUTPUT_FILE, "w") as test:
        s = 0
        for c in lengths:
            for i in range(c):
                print("{}/{}".format(s + 1, sum(lengths)), end="\r")

                path, height, width, xmin, ymin, xmax, ymax, class_name, class_id = output[s]

                if xmin >= xmax or ymin >= ymax or xmax > width or ymax > height or xmin < 0 or ymin < 0:
                    print("Warning: {} contains invalid box. Skipped...".format(path))
                    continue

                row = "{} {},{},{},{}\n".format(
                    path, xmin, ymin, xmax, ymax, class_id)
                if i <= c * SPLIT_RATIO:
                    train.writelines(row)
                else:
                    test.writelines(row)

                s += 1

    print("\nDone!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        input_folder = 'data'
    else:
        input_folder = sys.argv[1]

    main(input_folder)
