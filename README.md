# Ollama Function Calling Demo

This demo shows how to use Ollama with the Deepseek-r1 model to implement function calling capabilities.

## Prerequisites

1. Make sure you have access to a remote Ollama server or run Ollama locally
2. The remote Ollama server should have the Deepseek-r1 70B model available

## Setup

1. Create a new conda environment:
   ```bash
   conda create -n ollama-demo python=3.10
   conda activate ollama-demo
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

By default, the demo connects to Ollama at `http://localhost:11434`. To use a different Ollama server:

1. Modify the `base_url` parameter in `ollama_function_demo.py` to point to your Ollama server:
   ```python
   llm = Ollama(
       model="deepseek-r1:70b",
       base_url="http://your-ollama-server:11434",
       callbacks=[StreamingStdOutCallbackHandler()],
       temperature=0
   )
   ```

## Running the Demo

1. Make sure your Ollama server is accessible
2. Run the demo script:
   ```bash
   python ollama_function_demo.py
   ```

The demo includes two example functions:
- `get_current_weather`: A mock weather function that returns weather data for a given location
- `calculator`: A basic arithmetic calculator that can perform addition, subtraction, multiplication, and division

The script will process example queries and demonstrate how the model can understand when to call these functions and with what parameters.
