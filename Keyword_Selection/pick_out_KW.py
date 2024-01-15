"""
Input: Dialogue text, Keywords
Output: Add a column to the dialogue named "QA keywords"
Format: Q-keyowrd, A-keyword,...

Algorithm:   
Concat the Qs and As into two string
Split the relations and search them in the Qs
if found then search the entity text in the Qs
Search each splited entity in the As 
"""
import pandas as pd
import jieba
import pickle
import os
from tqdm import tqdm

def entity_search(entity_list:list, sentence:str)->list:
    keyword_list = []

    for entity in entity_list:
        if entity in sentence:
            keyword_list.append(entity)
    

    # Remove the stop words
    elements_to_remove = ['有','是','个','明','中','的','可','清','瓶','数','量']

    new_keyword_list = [x for x in keyword_list if x not in elements_to_remove]
    
    return new_keyword_list

splited_rel_keywords = {}

with open('KG_tail_prediction\\data\\relations_for_different_category\\category_refined_text_new.pkl', 'rb') as file:
    rel_text = pickle.load(file)

with open('keyword_dict.pkl', 'rb') as file:
    keyword_dict = pickle.load(file)

for key in rel_text.keys():
    rel_text_instance = rel_text[key]
    for relations in rel_text_instance:

        if relations in splited_rel_keywords.keys():
            continue

        splited_relations = jieba.cut(str(relations))
        splited_relations = list(splited_relations)

        splited_rel_keywords[relations] = splited_relations

elements_to_remove = ['有','是','个','明','中','的','可','清','瓶','数','量']

file_folders = {'label_100', 'label_25', 'label_50', 'label_75', 'label_0'}

for file_folder in file_folders:
    for i in tqdm(range(1, 3500)):
        file_path = "dialogue_{}.csv".format(i)
        if not os.path.exists(file_path):
            continue
        df = pd.read_csv(file_path)

        dialogue_len = df.shape[0]
        third_category = df.iloc[0, 10]
        keyword = keyword_dict[third_category]

        Q_keywords = []
        A_keywords = []

        Q_str = ""
        A_str = ""

        for j in range(0, dialogue_len):
            if df.iloc[j, 5] == 0:
                Q_str += df.iloc[j, 4]
            else:
                A_str += df.iloc[j, 4]
        
        # Search the keywords in Qs
        for rel_key in keyword.keys():
            splited_key = splited_rel_keywords[rel_key]

            if rel_key in Q_str:
                Q_keywords.append(rel_key)
                Q_keywords += entity_search(keyword[rel_key], Q_str)
                continue

            for item in splited_key:
                if item in elements_to_remove:
                    continue
                if item in Q_str:
                    Q_keywords.append(item)

        # Search the keywords in As
        for rel in keyword.keys():
            A_keywords += entity_search(keyword[rel], A_str)

        Q_keywords = list(set(Q_keywords))
        A_keywords = list(set(A_keywords))
        
        
        Q_keyword_str = "Q:"
        A_keyword_str = "A:"
        
        for item in Q_keywords:
            Q_keyword_str += item
            Q_keyword_str += ";"
        
        for item in A_keywords:
            A_keyword_str += item
            A_keyword_str += ";"

        df['keywords'] = Q_keyword_str + A_keyword_str

        saved_file_path = "dialogues_added_keywords/dialogue_{}.csv".format(file_folder, i)

        df.to_csv(saved_file_path)
  
    





