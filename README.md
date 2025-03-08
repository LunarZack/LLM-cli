# LLM CLI

A very simple command-line interface for interacting with AI models via OpenRouter's API.

## Overview

A terminal-based chat interface for communicating with language models through the OpenRouter API service. It features:

- Stream-based responses
- Simple conversation history management
- Clean, intuitive command-line interface
- simple API key handling

## Installation

### Prerequisites

- Python 3.6+
- `requests` library
- `python-dotenv` library

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

3. Create a `.env` file in the project directory with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-yourapikey
   ```

## Usage

Run the script from your terminal:

```bash
python llm-cli.py
```

- Type your message and press Enter to send it
- The AI will respond in real-time with streamed output
- Type `exit` to end the conversation

## Configuration

You can modify the following settings in the script:

- `MODEL_NAME`: Change the model you're using (default: "deepseek/deepseek-r1:free")
- Modify the payload options (like temperature, max_tokens, etc.) for different response behavior

## Security Notes

- API keys are stored in a local `.env` file that is not committed to Git
- Always add `.env` to your `.gitignore` file to prevent accidentally exposing your API key
- For production use, consider using a more robust secrets management solution

## Code Structure

The main components of the code include:

- Environment variable loading for secure API key management
- The `ask_question()` function that handles API communication and streaming responses
- The `start_conversation()` function that manages the chat interface loop
- JSON response parsing to handle streamed chunks correctly

## Troubleshooting

If you encounter issues:

- Ensure your API key is valid and has sufficient credits
- Check if the model name is correctly specified
- Verify your internet connection
- Look for any API error messages in the response

## Acknowledgements

- [OpenRouter](https://openrouter.ai/) for providing API access
- [DeepSeek AI](https://deepseek.ai/) for their language models