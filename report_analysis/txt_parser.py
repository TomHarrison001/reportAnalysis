"""Details of the structure of excel files, extract data into objects with properties"""

import re
import pandas as pd
import numpy as np
from gensim.parsing.preprocessing import remove_stopwords, strip_tags, strip_punctuation, strip_multiple_whitespaces, strip_short, strip_numeric
from gensim.parsing.porter import PorterStemmer
import pickle

import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import BertTokenizer
# from keras.preprocessing.sequence import pad_sequences

def ExtractData(import_file, sheet_name, na_filter=False):
    data = {}
    for key in ['NA', 'NC', 'NE', 'NH', 'NL', 'NN', 'NR', 'NS', 'NW']:
        data[key] = [0, 0, 0]
    whole = pd.read_excel(import_file, sheet_name=sheet_name, na_filter=na_filter)
    dataframe = whole[['Grounds', 'NPA']].copy()

    modelIntell = pickle.load(open('H://NLP//Val_Data//Pickled Trained Models//Intell_model.pkl', 'rb'))
    modelInit = pickle.load(open('H://NLP//Val_Data//Pickled Trained Models//Initiated_model.pkl', 'rb'))
    [val_dataloader, raw_dataframe] = ParseData(dataframe)
    InitPreds = evalModel(modelInit, val_dataloader)
    IntellPreds = evalModel(modelIntell, val_dataloader)
    predictions = pd.DataFrame({"Initiated": InitPreds, "Intell": IntellPreds})
    predictions = createMultiLab(predictions)
    dataframe['class'] = predictions

    # RandomiseData(dataframe)

    for index, row in dataframe.iterrows():
        if (not row['NPA'] in data):
            continue
        data[row['NPA']][int(row['class'])] += 1
    return data


def RandomiseData(dataframe):
    # 0 - incident response, 1 - officer discretion, 2 - intelligence led
    dataframe['class'] = np.random.randint(0, 3, dataframe.shape[0])
    

def ParseData(dataframe):
    raw_data = dataframe['Grounds'].astype(str).tolist()
    tokens = Preprocess(raw_data)
    raw_dataframe = pd.DataFrame({'Grounds': raw_data})
    token_dataframe = pd.DataFrame({'Grounds': tokens})
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    sequences = []
    for sent in token_dataframe['Grounds']:
        tokenized_sent = tokenizer.encode(sent, max_length=512)
        sequences.append(tokenized_sent)
    sequences = pad_sequences(sequences, maxlen=64, dtype="long", value=0, truncating="post", padding="post")
    attention_masks = []
    for sent in sequences:
        mask = [int(token_id > 0) for token_id in sent]
        attention_masks.append(mask)
    val_inputs = torch.tensor(sequences)
    val_masks = torch.tensor(attention_masks)
    val_data = TensorDataset(val_inputs, val_masks)
    val_sampler = SequentialSampler(val_data)
    batch_size = 16
    val_dataloader = DataLoader(val_data, sampler=val_sampler, batch_size=batch_size)
    return val_dataloader, raw_dataframe


def Preprocess(data):
    replacements = {
        r'redacted': '',
        r'Tango Victor': 'cctv',
        'TV': 'cctv',
        r'mop': 'member of public',
        'Op': 'operation',
    }
    stemmer = PorterStemmer()
    tokens_cleaned = []

    for token in range(0, len(data)):
        token = strip_tags(data[token]).lower()
        for method in [strip_punctuation, strip_multiple_whitespaces, strip_numeric, remove_stopwords, strip_short]:
            token = method(token)
        for key, value in replacements.items():
            token = re.sub(key, value, token)
        token = stemmer.stem(token)
        tokens_cleaned.append(token)

    return tokens_cleaned

def createMultiLab(dataframe):
    labs = []
    for index, row in dataframe.iterrows():
        if(row['Initiated'] == 0):
            # Incident response
            lab = 0
        elif(row['Intell'] == 0):
            # Officer discretion
            lab = 1
        else:
            # Intelligence led
            lab = 2 
        labs.append(lab)
    
    dataframe['class'] = labs
    return dataframe['class']
