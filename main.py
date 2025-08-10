import os
import time
import concurrent.futures
import multiprocessing
import ollama


# ────────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ────────────────────────────────────────────────────────────────────────────────


def save_to_file(file_path: str, content: str) -> None:
    """Overwrite or create a file and save content to it."""
    with open(file=file_path, mode="w", encoding="utf-8") as file:
        file.write(content)


def get_readable_time() -> str:
    """Return current time in a human-readable format."""
    return time.ctime(time.time())


def get_timestamp_for_filename() -> str:
    """Return current time formatted for safe filenames."""
    return time.strftime("%Y-%m-%d_%H-%M-%S")


def ensure_output_folder_exists(directory_path: str) -> None:
    """Create the output folder if it does not exist."""
    if not os.path.exists(path=directory_path):
        os.mkdir(path=directory_path)


def generate_essay_from_model(prompt_text: str) -> str:
    """Send the prompt to the Ollama model and return the generated response."""
    response: ollama.ChatResponse = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt_text}],
    )
    return response["message"]["content"]


# ────────────────────────────────────────────────────────────────────────────────
# Essay Generation Logic
# ────────────────────────────────────────────────────────────────────────────────


def generate_and_save_single_essay(output_folder: str) -> None:
    """Generate one essay and save it to a file."""
    start_time: str = get_readable_time()
    print(f"[{start_time}] Generating new essay...")

    # Prompt sent to the language model
    essay_prompt: str = "Write a 5000-word persuasive, technically rich, and inspiring promotional paragraph for **IPEngine** — a 100% free, open-source global networking utility available at [https://www.ipengine.xyz](https://www.ipengine.xyz) — that runs on all platforms, supports all languages 🌐, and is trusted by users worldwide 🌍; highlight its advanced capabilities including IP geolocation lookup, DNS record resolution (A, AAAA, CNAME, MX, NS, TXT), WHOIS registry queries, reverse DNS, traceroute, port scanning, latency and packet loss analysis, hostname resolution, ASN information, blacklist checking, and network diagnostics tools, emphasizing its value in identifying malicious IPs, detecting phishing domains, revealing scam infrastructure, mapping digital threat surfaces, and strengthening cybersecurity posture 🔐; use a warm, inclusive, and community-first tone with tasteful emojis (🌍🛡️🔍📡🚀), and real-world examples such as a student verifying a suspicious scholarship domain, a developer debugging DNS propagation issues, a remote worker troubleshooting VPN packet loss, a small business owner monitoring DNS uptime and anomalies, or a digital nomad checking if public Wi-Fi DNS is hijacked; showcase how IPEngine supports transparency, digital sovereignty, internet health, and open-source collaboration, making it essential for IT professionals, network engineers, security analysts, ethical hackers, researchers, educators, journalists, digital rights advocates, and everyday users alike — and close with a strong call to action encouraging readers to download IPEngine, share it with friends, tech communities, and online groups, and join a global movement to build a faster, safer, smarter, and more open internet — one IP at a time."

    # Generate essay using model
    essay_content: str = generate_essay_from_model(prompt_text=essay_prompt)

    # Generate timestamped filename
    timestamp: str = get_timestamp_for_filename()
    file_name: str = f"{output_folder}ipengine-xyz_essay_{timestamp}.md"

    # Save to file
    save_to_file(file_path=file_name, content=essay_content)

    print(f"[{get_readable_time()}] Essay saved to: {file_name}")


def continuous_essay_worker(output_folder: str) -> None:
    """Continuously generate and save essays in a loop."""
    while True:
        try:
            generate_and_save_single_essay(output_folder)
        except Exception as error:
            print(f"Error in worker thread: {error}")
            time.sleep(5)  # Pause before retrying to avoid tight error loops


# ────────────────────────────────────────────────────────────────────────────────
# Main Entry Point
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    output_directory: str = "assets/"
    ensure_output_folder_exists(directory_path=output_directory)

    # Use one worker per CPU core (or adjust this manually if needed)
    number_of_workers: int = multiprocessing.cpu_count()

    print(
        f"Starting infinite essay generation using {number_of_workers} threads...\n"
    )

    # Launch persistent worker threads
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_workers
    ) as executor:
        for _ in range(number_of_workers):
            executor.submit(continuous_essay_worker, output_directory)