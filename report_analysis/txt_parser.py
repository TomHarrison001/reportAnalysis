"""Details of the structure of excel files, extract data into objects with properties"""

import re
import pandas as pd
import numpy as np
from gensim.parsing.preprocessing import remove_stopwords, strip_tags, strip_punctuation, strip_multiple_whitespaces, strip_short, strip_numeric
from gensim.parsing.porter import PorterStemmer

import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import BertTokenizer
# from keras.preprocessing.sequence import pad_sequences

def ExtractData(import_file, sheet_name, na_filter=False):
    D = {}
    for key in ['NA', 'NC', 'NE', 'NH', 'NL', 'NN', 'NR', 'NS', 'NW']:
        D[key] = [0, 0, 0]
    whole = pd.read_excel(import_file, sheet_name=sheet_name, na_filter=na_filter)
    df = whole[['Grounds', 'NPA']].copy()
    # ParseData(df)
    RandomiseData(df)
    for index, row in df.iterrows():
        if (not row['NPA'] in D):
            continue
        D[row['NPA']][int(row['class'])] += 1
    return D


def RandomiseData(df):
    # 0 - incident response, 1 - officer discretion, 2 - intelligence led
    df['class'] = np.random.randint(0, 3, df.shape[0])
    

def ParseData(df):
    all_tokens_not_cleaned = df['Grounds'].astype(str).tolist()
    T = Preprocess(all_tokens_not_cleaned)
    df_T = pd.DataFrame({'Grounds': T, 'Lab': labs_code})
    unProcessedDF = pd.DataFrame({'Grounds': all_tokens_not_cleaned, 'Lab': labs_code})
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    V_input_ids = []
    V_attention_masks = []
    for sent in df_T['Grounds']:
        V_encoded_sent = tokenizer.encode(sent, max_length=512)
        V_input_ids.append(V_encoded_sent)
    V_input_ids = pad_sequences(V_input_ids, maxlen=64, dtype='long', value=0, truncating='post', padding='post')
    for sent in V_input_ids:
        att_mask = [int(token_id > 0) for token_id in sent]
        V_attention_masks.append(att_mask)
    val_inputs = torch.tensor(V_input_ids)
    val_masks = torch.tensor(V_attention_masks)
    val_labels = torch.tensor(labs_code)
    val_data = TensorDataset(val_inputs, val_masks, val_labels)
    val_sampler = SequentialSampler(val_data)
    batch_size = 16
    val_dataloader = DataLoader(val_data, sampler=val_sampler, batch_size=batch_size)
    return val_dataloader, unProcessedDF


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

    for sen in range(0, len(data)):
        doc = strip_tags(data[sen]).lower()
        for method in [strip_punctuation, strip_multiple_whitespaces, strip_numeric, remove_stopwords, strip_short]:
            doc = method(doc)
        for key, value in replacements.items():
            doc = re.sub(key, value, doc)
        doc = stemmer.stem(doc)
        tokens_cleaned.append(doc)

    return tokens_cleaned
