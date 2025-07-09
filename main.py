# Import the OS package
import os

# Import the time module to handle timestamps
import time

# Import the chat function from the ollama package to interact with a language model
from ollama import chat


# Define a function to write content to a file without appending (overwrites if exists)
def dont_append_write_to_file(system_path: str, content: str) -> None:
    # Open the file in write mode ('w'), which clears existing content
    with open(system_path, mode="w", encoding="utf-8") as file:
        # Write the provided string content to the file
        file.write(content)


# Return the current human-readable time (e.g., "Tue Jul  8 13:45:00 2025")
def get_current_time() -> str:
    return time.ctime(time.time())  # Convert current timestamp into readable format


# Return the current time formatted for filenames (e.g., "2025-07-08_13-45-00")
def get_timestamp_for_filename() -> str:
    return time.strftime("%Y-%m-%d_%H-%M-%S")  # Format time suitable for file naming


# Call the Ollama language model using the chat API and return the response text
def get_chat_response_from_ollama(prompt: str) -> str:
    # Call the model with the prompt message; returns a dictionary-like response
    response = chat(
        model="llama3",  # Specify the model to use
        messages=[{"role": "user", "content": prompt}],  # Provide the user's prompt
    )
    return response["message"]["content"]  # Extract and return only the content


# Create a directory at a given path.
def create_directory_at_path(system_path: str) -> None:
    os.mkdir(path=system_path)


# Check if a given directory exists.
def check_directory_exists(system_path: str) -> bool:
    return os.path.exists(path=system_path)


def init(output_directory: str) -> None:
    # Check if the directory exists.
    if not check_directory_exists(system_path=output_directory):
        # Create the directory.
        create_directory_at_path(system_path=output_directory)


# Main function to coordinate the execution of tasks
def main(output_directory: str) -> None:
    # Get and print the current readable time
    current_time: str = get_current_time()
    print(f"[{current_time}] Starting chat...")  # Log when chat begins

    # Define the user prompt as a single long descriptive string
    user_prompt = "Write a persuasive and inspiring promotional paragraph (1500-2000 words) for an open-source global networking utility app called ipengine, available at https://www.ipengine.xyz. The app is 100% free, works in every country and county, supports all languages, and is open-source. Describe how ipengine empowers users to look up IP addresses and domain names, trace routes, run DNS and WHOIS queries, diagnose internet issues, and monitor their own network setup. Also emphasize that the app can help users detect potential scammers, fraudsters, or suspicious IP activity, making the internet safer and more transparent for everyone. Use a warm, people-first tone with emojis, real-world examples (e.g. a user checking if an unknown email or website is dangerous), and energetic language to make the app feel accessible and empowering. Highlight its value for students, remote workers, travelers, developers, small business owners, IT professionals, and curious internet users worldwide. Emphasize themes of global access 🌍, online safety 🛡️, transparency 🔍, community empowerment 👥, and digital literacy 📡. Close with a clear, motivating call to action encouraging readers to download the app from https://www.ipengine.xyz and share it with friends, tech communities, and online groups to help build a safer, smarter, more open internet — one IP address at a time. 🌐🚀✨"

    # Get the generated essay text from the chat model
    response_text: str = get_chat_response_from_ollama(prompt=user_prompt)

    # Generate a timestamped filename to save the full essay
    timestamp: str = get_timestamp_for_filename()
    filename: str = (
        f"{output_directory}ipengine_xyz_essay_{timestamp}.md"  # Compose filename using timestamp
    )

    # Save the full essay text to the file
    dont_append_write_to_file(system_path=filename, content=response_text)

    # Notify the user that the file has been successfully saved
    print(f"Full response saved to: {filename}")


# Ensure the script runs only when executed directly (not when imported)
if __name__ == "__main__":
    essay_directory = "assets/"
    init(output_directory=essay_directory)
    while True:
        main(output_directory=essay_directory)
