```
  /$$$$$$            /$$        /$$$$$$  /$$      /$$$$$$
 /$$__  $$          | $$       /$$__  $$| $$     |_  $$_/
 $$  \ $$  /$$$$$$$| $$   /$$| $$  \__/| $$       | $$  
 $$$$$$$$ /$$_____/| $$  /$$/| $$      | $$       | $$  
 $$__  $$|  $$$$$$ | $$$$$$/ | $$      | $$       | $$  
 $$  | $$ \____  $$| $$_  $$ | $$    $$| $$       | $$  
 $$  | $$ /$$$$$$$/| $$ \  $$|  $$$$$$/| $$$$$$$$/$$$$$$
__/  |__/|_______/ |__/  \__/ \______/ |________/______/
```
A very minimal interface for interacting with AI models via OpenRouter's API.

## Overview
A minimal chat interface for communicating with language models through the OpenRouter API service. Using:
- Stream-based responses
- Simple conversation history management
- Clean, intuitive command-line interface
- Simple API key handling
- **Conversation saving and loading functionality**

## Installation

### Prerequisites
- Python 3.6+
- `requests` library
- `python-dotenv` library (optional)

### Setup
1. Clone this repository:
 ```bash
git clone https://github.com/lunarzack/llm-cli.git
cd llm-cli
 ```
2. Install the required dependencies:
 ```bash
pip install requests python-dotenv
 ```
3A. Create a `.env` file in the project directory with your OpenRouter API key:
 ```
 OPENROUTER_API_KEY=sk-or-v1-yourapikey
 ```
3B. Or hardcode it without using .env files on line 8:
 ```
 API_KEY = 'sk-or-v1-yourkeyhere'
 ```

## Usage
Run the script from your terminal:
```bash
./start.sh
```
OR
```bash
python llm-cli.py
```

### Basic Commands
- Type your message and press Enter to send it
- The AI will respond in real-time with streamed output
- Use the following commands:
  - `/exit` - End the conversation
  - `/save [name]` - Save the current conversation (with optional name)
  - `/load <filename>` - Load a previously saved conversation
  - `/list` - View all saved conversations

### Conversation Management
All conversations are saved in a `convo_hist` directory in JSON format. The directory is automatically created if it doesn't exist.

- When using `/save` without a name, a timestamp-based filename is generated
- When using `/load`, you can specify just the filename or the full path
- The `/list` command shows all available saved conversations with numbers for easy reference

## Configuration
You can modify the following settings in the script:
- `MODEL_NAME`: Change the model you're using (default: "deepseek/deepseek-chat:free"). Models can be found at [OpenRouter](https://openrouter.ai/models).
- Modify the payload options (like temperature, max_tokens, etc.) for different response behavior

## Code Structure
The main components of the code include:
- Environment variable loading for secure API key management
- The `ask_question()` function that handles API communication and streaming responses
- The `start_conversation()` function that manages the chat interface loop
- The `save_conversation()` and `load_conversation()` functions for conversation persistence
- JSON response parsing to handle streamed chunks correctly

## Troubleshooting
If you encounter issues:
- Ensure your API key is valid and has sufficient credits
- Check if the model name is correctly specified
- Look for any API error messages in the response
- If you have issues loading a conversation, ensure the file exists and is valid JSON

## Acknowledgements
- [OpenRouter](https://openrouter.ai/) for providing API access
- [DeepSeek AI](https://deepseek.ai/) for their language models