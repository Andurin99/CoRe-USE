"""
Input: Third Category
Output: Linked entities(List),  Related relations(List), packed as a file
"""

"""
In short of: 
- Category table(First category, Second category, Third category)
"""

"""
Read the Category table
Read the entity linking table
Get the linked entities according to the linking table
Get the first category according to the third category
Get relations according to the first category
"""
import pickle
import pandas as pd
import jieba

def relations_compare(first_category:str) -> str:
    """
    Get the exact first category according to the category text
    """

    category_dict = {1:"家用电器", 2:"电脑办公", 3:"汽车用品", 4:"数码", 5:"医药类",
                     6:"食品类", 7:"母婴", 8:"美容护肤", 9:"护理保健", 10:"服饰内衣"}

    words = jieba.cut(str(first_category))
    word_list = list(words)

    for word in word_list:
        for key in category_dict.keys():
            if word in category_dict[key]:
                return key
    
    return 11

def get_linked_entities(linking_table:pd.DataFrame, third_category_text:str) -> list:
    """
    Get the linked entities according to the third category
    """
    ent_text = []
    ent_index = []
    is_found = 0

    tab_len = linking_table.shape[0]

    for i in range(0, tab_len):
        topic = str(linking_table.iloc[i, 0])
        if topic == str(third_category_text):
            is_found = 1
            break
    
    if not is_found:
        return None
    
    for j in range(1, 20):
        if pd.isnull(linking_table.iloc[i,j]):
            break
        if "ent_" in linking_table.iloc[i, j]:
            ent_index.append(linking_table.iloc[i, j])
        else:
            ent_text.append(linking_table.iloc[i, j])
    
    ent_index = list(set(ent_index))
    ent_text = list(set(ent_text))

    return ent_index

def get_related_relations(relation_table:dict, category_table:dict, third_category_text:str) -> list:
    """
    Get the relations that related with the category
    """
    if third_category_text in category_table.keys():
        first_cate_text = category_table[third_category_text][0]
        rel_judge = relations_compare(first_cate_text)
    else:
        return relation_table[11]

    return list(set(relation_table[rel_judge] + relation_table[11]))

def EL_RC(third_category:str) -> str:
    category_indexes = "1-家用电器、2-电脑办公、3-汽车用品、4-数码、5-医药类、6-食品类、7-母婴、8-美容护肤、9-护理保健、10-服饰内衣、11-通用关系、12-其他"
    rel_index = []
    rel_text = []

    # Read the relations file
    with open('KG_tail_prediction\\data\\relations_for_different_category\\category_refined_rel_new.pkl', 'rb') as file:
        rel_index = pickle.load(file)

    # Read the product classification file 
    with open('KG_tail_prediction\\data\\relations_for_different_category\\category_table.pickle', 'rb') as file:
        category_table = pickle.load(file)

    # Read the entity link file
    linking_table = pd.read_csv('KG_tail_prediction\\data\\Entity_linking\\product_to_entity_examples.csv', header=None)

    linked_entities = get_linked_entities(linking_table, third_category)
    related_relations = get_related_relations(rel_index, category_table, third_category)

    if linked_entities == None:
        print("Cannot find out the entity!")
        return None, None
    
    return linked_entities,related_relations
