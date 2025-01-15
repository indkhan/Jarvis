
import asyncio
from voice_handler import listen, speak
from command_processor import execute_command
from config import load_config

async def main():
    """Main function to run Jarvis"""
    config = load_config()
    speak("Hello! I'm Jarvis, your AI assistant. How can I help you?")
    
    while True:
        command = listen()
        if command:
            if "goodbye" in command or "bye" in command:
                speak("Goodbye!")
                break
            
            result = execute_command(command, config)
            
            if isinstance(result, dict) and result.get('status') == 'error':
                speak(f"Sorry, there was an error: {result['message']}")
            else:
                speak("Task completed successfully")

if __name__ == "__main__":
    asyncio.run(main())