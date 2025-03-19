from dotenv import load_dotenv
import requests
import json
import os
import datetime
import time

load_dotenv()
API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL_NAME = "deepseek/deepseek-r1:free"

# Create directory for saving conversations if it doesn't exist
os.makedirs("convo_hist", exist_ok=True)

def save_conversation(conversation_history, filename=None):
    """
    Save the current conversation to a file
    
    Args:
        conversation_history: List of message dictionaries
        filename: Optional custom filename, if None will use timestamp
    
    Returns:
        str: Path to the saved file
    """
    # Create a timestamp-based filename if none provided
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    
    # Ensure the filename has .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Create the full path
    filepath = os.path.join("convo_hist", filename)
    
    # Save the conversation history to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conversation_history, f, indent=2, ensure_ascii=False)
    
    return filepath

def load_conversation(filepath):
    """
    Load a conversation from a file
    
    Args:
        filepath: Path to the conversation file
    
    Returns:
        list: The loaded conversation history
    """
    # If only filename is provided, add the directory
    if not os.path.dirname(filepath):
        filepath = os.path.join("convo_hist", filepath)
    
    # Ensure the file exists
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found")
        return None
    
    # Load the conversation history from the file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conversation_history = json.load(f)
        return conversation_history
    except json.JSONDecodeError:
        print(f"Error: File {filepath} is not a valid JSON file")
        return None

def list_saved_conversations():
    """
    List all saved conversations in the convo_hist directory
    
    Returns:
        list: List of saved conversation filenames
    """
    files = [f for f in os.listdir("convo_hist") if f.endswith('.json')]
    return sorted(files)

def ask_question(question, conversation_history):
    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": question})
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": conversation_history,
        "stream": True
    }
    print(f"\n{MODEL_NAME}:")
    # This will store the complete assistant response
    full_response = ""
    try:
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()  # Raise exception for bad status codes
            buffer = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if not chunk:
                    continue
                if chunk.startswith('data: '):
                    data = chunk[6:]
                    if data == '[DONE]':
                        break
                    try:
                        data_obj = json.loads(data)
                        content = data_obj["choices"][0]["delta"].get("content", "")
                        if content:
                            # Cleans up any problematic characters or emojis
                            cleaned_content = ''.join(char for char in content if ord(char) < 128)
                            print(cleaned_content, end="", flush=True)
                            full_response += cleaned_content
                    except json.JSONDecodeError:
                        pass
            print("\n")
            if full_response:
                conversation_history.append({"role": "assistant", "content": full_response})
            return conversation_history
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return conversation_history

def start_conversation():
    conversation_history = []
    ascii_art = r'''
  /$$$$$$            /$$        /$$$$$$  /$$      /$$$$$$
 /$$__  $$          | $$       /$$__  $$| $$     |_  $$_/
| $$  \ $$  /$$$$$$$| $$   /$$| $$  \__/| $$       | $$  
| $$$$$$$$ /$$_____/| $$  /$$/| $$      | $$       | $$  
| $$__  $$|  $$$$$$ | $$$$$$/ | $$      | $$       | $$  
| $$  | $$ \____  $$| $$_  $$ | $$    $$| $$       | $$  
| $$  | $$ /$$$$$$$/| $$ \  $$|  $$$$$$/| $$$$$$$$/$$$$$$
|__/  |__/|_______/ |__/  \__/ \______/ |________/______/
-----------------------------------------------------------'''
    print("\033[96m" + ascii_art + "\033[0m")
    print(f"Starting conversation with {MODEL_NAME}.")
    print("Commands:")
    print("  /exit          - End the conversation")
    print("  /save [name]   - Save the conversation (optional name)")
    print("  /load <name>   - Load a conversation")
    print("  /list          - List saved conversations")
    print("-----------------------------------------------------------")
    
    while True:
        user_input = input("\nYou: ")
        
        # Check for commands
        if user_input.lower() == "/exit":
            print("Conversation ended.")
            break
            
        elif user_input.lower().startswith("/save"):
            # Extract optional filename
            parts = user_input.split(maxsplit=1)
            filename = parts[1] if len(parts) > 1 else None
            
            # Save the conversation
            saved_path = save_conversation(conversation_history, filename)
            print(f"Conversation saved to: {saved_path}")
            
        elif user_input.lower().startswith("/load"):
            # Extract filename
            parts = user_input.split(maxsplit=1)
            if len(parts) < 2:
                print("Error: Please specify a filename to load")
                continue
                
            filename = parts[1]
            
            # Load the conversation
            loaded_history = load_conversation(filename)
            if loaded_history:
                conversation_history = loaded_history
                print(f"Loaded conversation from: {filename}")
                # Print a summary of the loaded conversation
                print(f"Loaded {len(conversation_history)} messages")
                
        elif user_input.lower() == "/list":
            # List saved conversations
            saved_files = list_saved_conversations()
            if saved_files:
                print("Saved conversations:")
                for i, filename in enumerate(saved_files, 1):
                    print(f"  {i}. {filename}")
            else:
                print("No saved conversations found")
                
        else:
            # Regular message - send to the model
            conversation_history = ask_question(user_input, conversation_history)

if __name__ == "__main__":
    start_conversation()