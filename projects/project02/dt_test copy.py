import sys
from math import log
import os
import argparse
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("--train", help="train data file",  default='dt_train1.txt', type=str)
parser.add_argument("--test", help="test data file", default='dt_test1.txt', type=str)
parser.add_argument("--output", help="output path", default='dt_result1.txt', type=str)
args = parser.parse_args()

def load_data(file_path):
    df = pd.DataFrame(pd.read_csv(file_path, sep='\t'))
    df_data = np.array(df).tolist()
    return df_data

#Unused in current version
#Function when you don't have answer
def Datasplit(my_data, ratio=0.75):
    #Split the given train data
    #train and validation by a given ratio
    length_attr = len(my_data)
    length_row = len(my_data[0]) - 1

    cut = int(length_attr * ratio)
    train = my_data[:cut]
    validation = my_data[cut:]
    x_val = []
    [x_val.append(row[:length_row]) for row in validation]

    return train, x_val, validation
#Python object to make tree structure
#Resembles Clang's struct 
class Node:
    def __init__(self, attr=-1, att_value=None, results=None, left=None, right=None):
        self.attr = attr           #attribute number
        self.att_value = att_value #attribute value
        self.results = results     #Only for leaf
        self.left = left           #Points to left node
        self.right = right         #Points to right node


def RecursiveBuild(df):
    #Local function for entropy calculation
    def entropy(df):
        results = CountCheck(df)
        ent = 0.0
        for label in results:
            p = float(results[label]) / len(df)
            ent = ent - p * log(p) / log(2)
        return ent
    
    current_score = entropy(df)
    top_value = 0.0    #Information gain
    top_att = None     #Best attribute
    top_splits = None  #Best splitted two sets
    column_count = len(df[0]) - 1
    #loop through every attributes except label
    for attr in range(0, column_count):
        column_att_values = {}
        for row in df:
            column_att_values[row[attr]] = 1

        for att_value in column_att_values.keys():
            #Split based on certain value
            #Calculate information gain
            left = [row for row in df if row[attr] == att_value]
            right = [row for row in df if not row[attr] == att_value]

            p = float(len(left)) / len(df)
            gain = current_score - p * entropy(left) - (1 - p) * entropy(right)
            
            #Updates top_value and so on
            if gain > top_value and len(left) > 0 and len(right) > 0:
                top_value = gain
                top_att = (attr, att_value)
                top_splits = (left, right)
    #Repeat until the information gain get minus 
    if top_value > 0:
        Leftbranch = RecursiveBuild(top_splits[0])
        Rightbranch = RecursiveBuild(top_splits[1])
        #Recursively build decision tree 
        #using pre-defined node object
        return Node(attr=top_att[0], att_value=top_att[1], left=Leftbranch, right=Rightbranch)
    else:
        #When it reach leaf, count the number
        return Node(results=CountCheck(df))

#Count the number of leaf element
def CountCheck(tups):
    res = {}
    for t in tups:
        label = t[len(t)-1]
        if label not in res:
            res[label] = 0
        res[label] += 1
    return res


def Classifier(test_data, tree):
    #local function to classify each row
    def classify(row, tree):
        #When leaf node
        if tree.results:
            return tree.results
        else:
            #Follow from the root node to leaf
            v = row[tree.attr]
            branch = None
            if v == tree.att_value:
                branch = tree.left
            else:
                branch = tree.right

            #Repeat until it gets to the leaf
            return classify(row, branch)
    #Apply classify function to the whole test data
    for i in range(len(test_data)):
        #Make a prediction for each row
        classified = classify(test_data[i], tree).keys()
        test_data[i].append(list(classified)[0])

    return test_data


def WriteFile(test_data, f, header):
    attr_len = len(test_data)
    row_len = len(test_data[0])
    #Write first rows: header
    first = "\t".join(header)+"\n"
    f.write(first)
    #Unlist the array to meet
    #guided output format
    [f.write("\t".join(test_data[i]) + "\n") for i in range(attr_len)]
    return f


if __name__ == "__main__":
    train, test, result_name = args.train, args.test, args.output
    #Read train, test file
    data = load_data(train)
    test_a = load_data(test)
    header = data[0]        #Extract header for output's first row
    test = test_a[1:]       #Omit header row
    my_data = data[1:]      #Omit header row
    #Recursively find the best attribute 
    tree = RecursiveBuild(my_data)
    #Make a prediction based on trained decision tree
    result = Classifier(test, tree)
    #Make output file with given name
    out_file = open(result_name, 'w')
    #Write predictions on the output file
    Result = WriteFile(result, out_file, header)
    out_file.close()
    os.system('dt_test.exe dt_answer1.txt dt_result1.txt')