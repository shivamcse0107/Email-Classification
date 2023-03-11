import transformers
import torch
import yaml
import torch.nn as nn
from tqdm import tqdm
import logging
import pandas as pd
from read_params import read_params

logging.basicConfig(level=logging.ERROR)
CUDA_LAUNCH_BLOCKING=1

config = read_params('config.yaml')
TOKENIZER = transformers.BertTokenizer.from_pretrained(config['base']['BERT_PATH'], do_lower_case=True,truncation=True)
class BERTDataset:
    def __init__(self, text):
        self.text = text
        self.tokenizer = TOKENIZER
        self.max_len = config['base']['MAX_LEN']

    def __len__(self):
        return len(self.text)
    def __getitem__(self, item):
        text = str(self.text[item])
        text = " ".join(text.split())

        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding="max_length",
            truncation= True,
        )

        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
        }
class BERTBaseUncased(nn.Module):
    def __init__(self):
        super(BERTBaseUncased, self).__init__()
        self.bert = transformers.BertModel.from_pretrained(config['base']['BERT_PATH'])
        self.bert_drop = nn.Dropout(0.3)
        self.out = nn.Linear(768, int(config['base']['TARGET']))

    def forward(self, ids, mask, token_type_ids):
        _, o2 = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids,return_dict=False)
        bo = self.bert_drop(o2)
        output = self.out(bo)
        return output

def inference(data_loader, model, device):
    model.eval()
    fin_outputs = []
    with torch.no_grad():
        for bi, d in tqdm(enumerate(data_loader), total=len(data_loader)):
            ids = d["ids"]
            token_type_ids = d["token_type_ids"]
            mask = d["mask"]
            ids = ids.to(device, dtype=torch.long)
            token_type_ids = token_type_ids.to(device, dtype=torch.long)
            mask = mask.to(device, dtype=torch.long)
            outputs = model(ids=ids, mask=mask, token_type_ids=token_type_ids)
            fin_outputs.extend(torch.argmax(outputs,axis = 1).cpu().detach().numpy().tolist())
    return fin_outputs

labels = {0:'Approved Timesheet', 1:'Bank details', 2:'Invoicing', 3:'Others', 4:'Payment confirmation', 5:'Payment escalating', 6:'Payment follow up',7:'Payment status', 8:'Promise to pay'}

def Prediction_On_Body(data):
    dfx = pd.DataFrame([str(data)],columns=['Body'])
    test_dataset =BERTDataset(
        text=dfx['Body'].values
    )
    test_data_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=16, num_workers=4
    )
    device = torch.device(config['base']['DEVICE'])
    model = BERTBaseUncased()
    model.load_state_dict(torch.load(config['base']['MODEL_PATH']))
    model.to(device)
    output = inference(test_data_loader, model, device)
    return labels[output[0]]
    