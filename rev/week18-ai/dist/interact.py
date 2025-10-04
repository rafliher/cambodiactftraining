import torch
from model import ASCIIModel, vocab
import torch.nn as nn
import string

vocab = " " + string.ascii_lowercase

def encode_messages(messages, seq_length=32):
    ''' One-hot encode input messages.  '''
    # Create the tensor to hold the one-hot encoded inputs
    batch_size = len(messages)
    input_tensor = torch.zeros((batch_size, seq_length, len(vocab)))

    for i, msg in enumerate(messages):
        for j, char in enumerate(msg[:seq_length]):  # Truncate if longer than seq_length
            if char not in vocab:
                raise ValueError(f"Character '{char}' not in vocabulary")
            char_idx = vocab.index(char)
            input_tensor[i, j, char_idx] = 1
    return input_tensor

def decode_message(output_tensor):
    '''Decode the model's output tensor to human-readable text.'''
    # Take the argmax of logits to find the most likely character at each position
    max_indices = torch.argmax(output_tensor, dim=2)
    # Map the indices to characters
    predicted_chars = [''.join([vocab[idx] for idx in sequence]) for sequence in max_indices.cpu().numpy()]
    return predicted_chars

# Specify the device for model execution
device = torch.device("cpu") # Use 'cuda' for NVIDIA GPU or 'cpu' for CPU

# Load the pre-trained model with safe globals
with torch.serialization.safe_globals([ASCIIModel, torch.nn.modules.linear.Linear]):
    model = torch.load('model.pkl', map_location=device)

batch_size = 32 # Create 32 random input messages
seq_length = 32 # 32 characters in each input message
input_tensor = torch.randn(batch_size, seq_length, len(vocab), device=device, requires_grad=True)
true_labels = input_tensor.argmax(dim=2)

criterion = nn.CrossEntropyLoss(reduction='mean')
optimizer = torch.optim.Adam([input_tensor], lr=0.01)

# Optimization loop
for _ in range(1000):
    optimizer.zero_grad()  # Zero the gradients
    logits = model(input_tensor)  # Get model predictions
    loss = criterion(logits.transpose(1, 2), true_labels)  # Calculate loss
    (-loss).backward()  # Invert the gradient to maximize loss
    optimizer.step()  # Update the input tensor
    
# Decode and print the output messages
for i in range(batch_size):
    individual_input = input_tensor[i].unsqueeze(0)
    print(f"Input {i:<02}: {decode_message(individual_input)} -> {decode_message(model(individual_input))}")