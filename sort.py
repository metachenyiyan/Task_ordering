# Python program to print topological sorting of a DAG
import sys
import csv
from collections import defaultdict
from future.builtins import input

def feature_compare(feature):
    def compare(a, b):
        print("%s ? %s (> or <) for %s" % (a, b, feature))
        answer = input()
        while answer not in [">", "<"]:
            print("%s ? %s (> or <) for %s" % (a, b, feature))
            answer = input()
        if answer == ">":
            return 1
        if answer == "<":
            return -1
    return compare

def merge(a_list, b_list, comp):
    ia, ib = 0, 0
    new_list = []
    while ia < len(a_list) and ib < len(b_list):
        if comp(a_list[ia], b_list[ib]) > 0:
            new_list.append(a_list[ia])
            ia += 1
        else:
            new_list.append(b_list[ib])
            ib += 1
    out = new_list + a_list[ia:] + b_list[ib:]
    return out

def merge_sort(a_list, comp):
    if len(a_list) <= 1:
        return a_list
    mid = len(a_list) // 2
    return merge(merge_sort(a_list[:mid], comp), merge_sort(a_list[mid:], comp), comp)


def make_score(object_list, features, decay_ratio=0.9):
    feature2object2score = defaultdict(dict)
    for feature in features:
        object2score = feature2object2score[feature]
        sorted_list = merge_sort(object_list, feature_compare(feature))
        n = len(sorted_list)
        r = decay_ratio
        ttl = (pow(r, n) - 1)/(r-1)
        for i in range(0, n):
            object2score[sorted_list[i]] = pow(r, i)/ttl
    return feature2object2score

def make_score_io(filename, decay_ratio=0.9):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()
        features = header[1:]
        print(features)
        objects = [row[0] for row in reader]
    feature2object2score = make_score(objects, features, float(decay_ratio))
    print(feature2object2score)
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["objects"] + features)
        writer.writeheader()
        for object in objects:
            row = {feature: feature2object2score[feature][object] for feature in features}
            row["objects"] = object
            writer.writerow(row)

make_score_io(*sys.argv[1:])


