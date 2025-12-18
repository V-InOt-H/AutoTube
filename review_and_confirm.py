import os
import subprocess
import sys

DATA_DIR = "data"

FILES = {
    "1": ("Title", os.path.join(DATA_DIR, "title.txt")),
    "2": ("Description", os.path.join(DATA_DIR, "description.txt")),
    "3": ("Hashtags", os.path.join(DATA_DIR, "hashtags.txt")),
    "4": ("Script", os.path.join(DATA_DIR, "script.txt")),
}

def read_file(path):
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return "(missing)"

def show_content():
    print("\n===== CURRENT CONTENT =====")
    for key, (label, path) in FILES.items():
        print(f"\n[{key}] {label}:")
        print("------------------------")
        print(read_file(path))
    print("\n===========================\n")

def edit_field():
    choice = input("Which one to edit? (1=Title, 2=Description, 3=Hashtags, 4=Script): ").strip()
    if choice in FILES:
        label, path = FILES[choice]
        print(f"Editing {label} ({path})...")
        subprocess.run(["nano", path])
    else:
        print("Invalid choice.")

def regenerate_ai():
    print("🔁 Regenerating using Ollama (script_caption_hashtags_ollama.py)...")
    result = subprocess.run([sys.executable, "script_caption_hashtags_ollama.py"])
    if result.returncode != 0:
        print("❌ Regeneration failed.")
        sys.exit(1)
    print("✅ Regenerated. Showing new content:")
    show_content()

def main():
    if not os.path.exists(DATA_DIR):
        print("No data/ directory yet. Run generator first.")
        sys.exit(1)

    show_content()

    while True:
        choice = input("[c] continue  [e] edit  [r] regenerate with AI  [q] quit: ").strip().lower()
        if choice == "c":
            print("✅ Confirmed. Continuing pipeline...")
            sys.exit(0)
        elif choice == "e":
            edit_field()
            show_content()
        elif choice == "r":
            regenerate_ai()
        elif choice == "q":
            print("❌ User aborted pipeline.")
            sys.exit(1)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
