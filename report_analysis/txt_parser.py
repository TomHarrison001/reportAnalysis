"""Details of the structure of excel files, extract data into objects with properties"""

from re import sub
from pandas import read_excel, DataFrame
from numpy import random, argmax
from gensim.parsing.preprocessing import remove_stopwords, strip_tags, strip_punctuation, strip_multiple_whitespaces, strip_short, strip_numeric
from gensim.parsing.porter import PorterStemmer
from pickle import load

import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import BertTokenizer
from keras.preprocessing.sequence import pad_sequences
from pathlib import Path

def ExtractData(import_file, sheet_name, na_filter=False):
    data = {}
    for key in ['NA', 'NC', 'NE', 'NH', 'NL', 'NN', 'NR', 'NS', 'NW']:
        data[key] = [0, 0, 0]
    whole = read_excel(import_file, sheet_name=sheet_name, na_filter=na_filter)
    dataframe = whole[['Grounds', 'NPA']].copy()

    root = Path(__file__).parent.parent / 'models'
    try:
        modelIntell = load(open(str(root / 'Intell_model.pkl'), 'rb'))
        modelInit = load(open(str(root / 'Initiated_model.pkl'), 'rb'))
    except Exception as e:
        raise Exception('Model files missing.')
    [val_dataloader, raw_dataframe] = ParseData(dataframe)
    InitPreds = EvalModel(modelInit, val_dataloader)
    IntellPreds = EvalModel(modelIntell, val_dataloader)
    predictions = DataFrame({"Initiated": InitPreds, "Intell": IntellPreds})
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
    dataframe['class'] = random.randint(0, 3, dataframe.shape[0])


def EvalModel(model, val_dataloader):
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    predictions = []
    for batch in val_dataloader:
        batch = tuple(t.to(device) for t in batch)
        b_input_ids, b_input_mask = batch
        with torch.no_grad():
            logits = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)
        logits = logits[0].detach().cpu().numpy()
        predictions.append(logits)
    
    flat_predictions = [item for sublist in predictions for item in sublist]
    flat_predictions = argmax(flat_predictions, axis=1).flatten()
    return flat_predictions


def ParseData(dataframe):
    raw_data = dataframe['Grounds'].astype(str).tolist()
    tokens = Preprocess(raw_data)
    raw_dataframe = DataFrame({'Grounds': raw_data})
    token_dataframe = DataFrame({'Grounds': tokens})
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    sequences = []
    for sent in token_dataframe['Grounds']:
        tokenized_sent = tokenizer.encode(sent, truncation=True, max_length=512)
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
            token = sub(key, value, token)
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
