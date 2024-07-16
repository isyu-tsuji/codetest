import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM, BertConfig
import os

# Load pre-trained tokenizer and model
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')

config = BertConfig.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
config.output_hidden_states = False  # Ignore weights

model = BertForMaskedLM.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking', config=config)

def correct_speech_text(text):
    # Tokenize input text and create masked tokens
    tokens = tokenizer.tokenize(text)
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    masked_input_ids = [tokenizer.mask_token_id if token == tokenizer.cls_token else token_id for token, token_id in zip(tokens, input_ids)]

    # Convert to PyTorch tensors
    input_ids = torch.tensor([input_ids])
    masked_input_ids = torch.tensor([masked_input_ids])

    # Get predictions from BERT model
    with torch.no_grad():
        outputs = model(input_ids, labels=masked_input_ids)
        predictions = outputs.logits

    # Get the predicted tokens
    predicted_token_ids = predictions.argmax(dim=-1).tolist()[0]
    predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_token_ids)

    # Reconstruct the corrected text
    corrected_text = tokenizer.convert_tokens_to_string(predicted_tokens)
    return corrected_text

def process_file(file_path, output_dir):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    corrected_text = correct_speech_text(text)

    output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".txt", "_corrected.txt"))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(corrected_text)
    return output_file

if __name__ == "__main__":
    transcription_dir = "transcriptions"
    corrected_dir = "corrected_transcriptions"
    if not os.path.exists(corrected_dir):
        os.makedirs(corrected_dir)

    for transcription_file in os.listdir(transcription_dir):
        if transcription_file.endswith(".txt"):
            process_file(os.path.join(transcription_dir, transcription_file), corrected_dir)