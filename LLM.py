import ollama

# Default model to use for LLM interactions
MODEL = "phi3:mini"

def collect_stream(response) -> str:
    """Collect full text from a streaming Ollama response.
    
    Args:
        response: A streaming response object from ollama.chat()
        
    Returns:
        Complete response text concatenated from all stream chunks
    """
    # Accumulate all chunks from the stream
    full_text = ""
    for chunk in response:
        # Extract message content from each chunk
        full_text += chunk.message.content
    return full_text

def run(prompt: str, text: str, model=MODEL, stream=True):
    """Run an LLM chat with optional streaming response.
    
    Args:
        prompt: The instruction or question to ask the LLM
        text: The text content to process with the prompt
        model: The Ollama model to use (default: phi3:mini)
        stream: Whether to stream the response (default: True)
        
    Returns:
        If stream=True: A streaming response object from Ollama
        If stream=False: Complete response text as a string
    """
    # Combine prompt and text into a single user message
    usr_mssg = [{"role": "system", "content": prompt},
                {"role": "user", "content": text}]
    
    # Send message to the LLM with specified streaming mode
    bot = ollama.chat(model=model, messages=usr_mssg, stream=stream)
    
    # Return the response (streaming object or full text depending on stream parameter)
    return bot