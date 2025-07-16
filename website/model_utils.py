import torch
from transformers import BartTokenizer, BartForConditionalGeneration

# Load model and tokenizer once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
model.load_state_dict(torch.load("BART.pth", map_location=device))
model.to(device)
model.eval()

def evaluate_input(text):
    inputs = tokenizer(text, return_tensors="pt").to(device)
    output_ids = model.generate(**inputs)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

def evaluate(model, tokenizer, input_text, device):
    model.eval()
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs)

    output = tokenizer.decode(outputs[0], skip_special_tokens=False)

    return tokenizer.decode(outputs[0], skip_special_tokens=True, truncation=False)