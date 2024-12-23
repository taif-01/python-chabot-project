import json
import time


class NaturalLanguageProcessor:
    """Handles text preprocessing for better input understanding."""

    @staticmethod
    def preprocess_input(user_input: str) -> str:
        """Normalize and clean user input."""
        return user_input.lower().strip()


class KnowledgeBase:
    """Manages responses and dynamically updates knowledge."""

    def __init__(self, knowledge_file: str = "knowledge_base.json"):
        self.responses = {}
        self.knowledge_file = knowledge_file
        self.load_knowledge(knowledge_file)  # Automatically load knowledge on initialization

    def get_response(self, user_input: str) -> str:
        """Fetch a response for the given user input."""
        return self.responses.get(user_input, "Sorry, I don't understand that.")

    def add_response(self, input_str: str, response: str) -> None:
        """Add a new response to the knowledge base."""
        self.responses[input_str] = response

    def load_knowledge(self, file_path: str) -> None:
        """Load knowledge from a JSON file."""
        try:
            with open(file_path, "r") as file:
                self.responses.update(json.load(file))
                print("Knowledge base loaded from file.")
        except FileNotFoundError:
            print(f"Knowledge file '{file_path}' not found. Starting fresh.")
        except json.JSONDecodeError:
            print("Error decoding JSON file. Please check its format.")

    def save_knowledge(self, file_path: str) -> None:
        """Save current knowledge to a JSON file."""
        try:
            with open(file_path, "w") as file:
                json.dump(self.responses, file, indent=4)
                print("Knowledge base saved to file.")
        except IOError:
            print("Error saving knowledge to file. Please try again.")


class Logger:
    """Logs the conversations for future reference."""

    def __init__(self):
        self.logs = []

    def log_message(self, user_input: str, bot_response: str) -> None:
        """Log a single message."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] User: {user_input} | Bot: {bot_response}"
        self.logs.append(log_entry)

    def get_logs(self) -> list:
        """Retrieve the conversation logs."""
        return self.logs

    def save_logs(self, file_path: str) -> None:
        """Save logs to a file."""
        try:
            with open(file_path, "w") as file:
                for log in self.logs:
                    file.write(log + "\n")
                print("Logs saved successfully.")
        except IOError:
            print("Error saving logs to file. Please try again.")

    def display_logs(self) -> None:
        """Print all logged conversations."""
        if not self.logs:
            print("No logs available.")
        else:
            print("\nConversation Logs:")
            for log in self.logs:
                print(log)


class Chatbot:
    """Central chatbot class for managing user interactions."""

    def __init__(self, name: str, knowledge_base: KnowledgeBase, logger: Logger):
        self.name = name
        self.knowledge_base = knowledge_base
        self.logger = logger
        self.nlp = NaturalLanguageProcessor()

    def process_message(self, message: str) -> str:
        """Process user message and return a response."""
        preprocessed_message = self.nlp.preprocess_input(message)
        response = self.knowledge_base.get_response(preprocessed_message)
        self.logger.log_message(preprocessed_message, response)
        return response


class UserInterface:
    """Handles interaction between the user and the chatbot."""

    def __init__(self, chatbot: Chatbot):
        self.chatbot = chatbot
        self.running = True  # To track if the program is active

    def main(self):
        """Main method to control the flow of the application."""
        print(f"Hi! I'm {self.chatbot.name}. Type 'Start' to begin or 'Exit' anytime to quit.")

        while self.running:
            user_input = input("You: ").strip().lower()

            if user_input == "start":
                self.show_main_menu()
            elif user_input == "exit":
                print("Have a Good day!")
                self.running = False
            else:
                print("Please type 'Start' to begin or 'Exit' to quit.")

    def show_main_menu(self):
        """Display the main menu options."""
        while True:
            print("\n1. Start Chatbot\n2. Add Knowledge\n3. Load Knowledge\n4. Save Knowledge\n5. View Knowledge\n6. View Logs\n7. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.start_chat()
            elif choice == "2":
                self.chatbot.admin_panel.add_knowledge()
            elif choice == "3":
                self.chatbot.admin_panel.load_knowledge()
            elif choice == "4":
                self.chatbot.admin_panel.save_knowledge()
            elif choice == "5":
                self.chatbot.admin_panel.view_knowledge()
            elif choice == "6":
                self.chatbot.logger.display_logs()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def start_chat(self):
        """Start a chat with the chatbot."""
        print(f"Hi! I'm {self.chatbot.name}. If you want anything from me, you can ask. Or type 'exit' to quit the chat.")
        while True:
            user_input = input("You: ").strip().lower()
            if user_input == "exit":
                print("Exiting chat... Anything else you want from me?")
                break

            response = self.chatbot.process_message(user_input)
            print(f"{self.chatbot.name}: {response}")

            # Ask if the answer is profitable
            follow_up = input("Is the answer profitable? Anything else you want from me? (Yes/No): ").strip().lower()

            if follow_up == "yes":
                print("Thank you for being with us.")
                break
            elif follow_up == "no":
                print("How can I help you?")
            else:
                print("Invalid input. Please respond with 'Yes' or 'No'.")


class AdminPanel:
    """Admin panel to manage the chatbot's knowledge base."""

    def __init__(self, knowledge_base: KnowledgeBase, knowledge_file: str = "knowledge_base.json"):
        self.knowledge_base = knowledge_base
        self.knowledge_file = knowledge_file

    def add_knowledge(self):
        """Add new entries to the knowledge base and save them permanently."""
        while True:
            input_str = input("Enter the user input: ").strip().lower()
            response = input("Enter the chatbot's response: ").strip()
            self.knowledge_base.add_response(input_str, response)
            self.knowledge_base.save_knowledge(self.knowledge_file)

            follow_up = input("New knowledge added and saved successfully! Anything else you want to add & save? (Yes/No): ").strip().lower()

            if follow_up == "yes":
                print("Ok, you are free to add.")
            elif follow_up == "no":
                print("Thank you for being with us.")
                break
            else:
                print("Invalid input. Please respond with 'Yes' or 'No'.")

    def load_knowledge(self):
        """Load the knowledge base from a file."""
        file_path = input("Enter the file path to load knowledge: ").strip()
        self.knowledge_base.load_knowledge(file_path)

    def save_knowledge(self):
        """Save the knowledge base to a file."""
        file_path = input("Enter the file path to save knowledge: ").strip()
        self.knowledge_base.save_knowledge(file_path)

    def view_knowledge(self):
        """View all responses in the knowledge base."""
        print("\nCurrent Knowledge Base:")
        for key, value in self.knowledge_base.responses.items():
            print(f"Input: {key} | Response: {value}")


def main():
    """Main function to run the chatbot system."""
    knowledge_file = "knowledge_base.json"  # File to store knowledge
    knowledge_base = KnowledgeBase(knowledge_file=knowledge_file)
    logger = Logger()
    chatbot = Chatbot(name="MiniGPT", knowledge_base=knowledge_base, logger=logger)
    admin_panel = AdminPanel(knowledge_base=knowledge_base, knowledge_file=knowledge_file)
    ui = UserInterface(chatbot=chatbot)

    chatbot.admin_panel = admin_panel  # Link admin panel to chatbot

    while True:
        print("\n1. Start Chatbot\n2. Add Knowledge\n3. Load Knowledge\n4. Save Knowledge\n5. View Knowledge\n6. View Logs\n7. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            ui.start_chat()
        elif choice == "2":
            admin_panel.add_knowledge()
        elif choice == "3":
            admin_panel.load_knowledge()
        elif choice == "4":
            admin_panel.save_knowledge()
        elif choice == "5":
            admin_panel.view_knowledge()
        elif choice == "6":
            logger.display_logs()
        elif choice == "7":
            print("Exiting... Goodbye! See you again.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
