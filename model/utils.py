from transformers import T5Tokenizer, T5ForConditionalGeneration
from config import *




def tokenize_data(data, tokenize):
    """
    Tokenize the input data for T5 fine-tuning.

    Args:
    - data (dict): A single datapoint from the dataset with `prompt` and `response`.
    - tokenizer (T5Tokenizer): Pretrained T5 tokenizer instance to tokenize the data.

    Returns:
    - dict: Tokenized `input_ids` and `labels`.
    """

    # Input to the model: 'prompt'
    input_text = data['prompt']

    # Expected output to the model: Flattened 'response' (as a string)
    response_dict = data['response']
    output_text = "course_stack: {course_stack}, course_number: {course_number}, course_name: {course_name}, course_code: {course_code}, faculty_name: {faculty_name}".format(
        course_stack=response_dict['course_stack'] or "null",
        course_number=response_dict['course_number'] or "null",
        course_name=response_dict['course_name'] or "null",
        course_code=response_dict['course_code'] or "null",
        faculty_name=response_dict['faculty_name'] or "null"
    )
    # Tokenizing the input prompt
    input_tokens = tokenize(input_text)

    # Tokenizing the response (output) 
    output_tokens = tokenize(output_text)
    # Return tokenized input and labels
    return {
        'input_ids': input_tokens['input_ids'],   # Tokenized input
        'attention_mask': input_tokens['attention_mask'],  # Attention mask for input
        'labels': output_tokens['input_ids']  # Tokenized labels (output)
    }



