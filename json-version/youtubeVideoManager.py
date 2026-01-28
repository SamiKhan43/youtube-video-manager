import json
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    try:
        with open("videos.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(videos):
    with open("videos.json", "w") as file:
        json.dump(videos, file, indent=2)

def list_all_videos(videos):
    if not videos:
        print("No videos found.")
        return
    for i, video in enumerate(videos, start=1):
        print("\n")
        print("*" * 70)
        print(f"{i}. Title      : {video['title']}")
        print(f"   URL        : {video['url']}")
        print(f"   Description: {video['description']}")
        print("*" * 70)
        print("\n")

def add_new_video(videos, user_name):
    title = input("Enter video title: ")
    url = input("Enter video URL: ")
    description = input("Enter video description: ")
    videos.append({
        "title": title,
        "url": url,
        "description": description
    })
    save_data(videos)
    print(f"{user_name}, video added successfully!")

def update_video(videos, user_name):
    list_all_videos(videos)
    if not videos:
        return
    try:
        index = int(input("Enter video number to update: ")) - 1
        if 0 <= index < len(videos):
            videos[index]['title'] = input("Enter new title: ")
            videos[index]['url'] = input("Enter new URL: ")
            videos[index]['description'] = input("Enter new description: ")
            save_data(videos)
            print(f"{user_name}, video updated successfully!")
        else:
            print(f"{user_name}, invalid video number.")
    except ValueError:
        print("Invalid input.")

def delete_video(videos, user_name):
    list_all_videos(videos)
    if not videos:
        return
    try:
        index = int(input("Enter video number to delete: ")) - 1
        if 0 <= index < len(videos):
            removed = videos.pop(index)
            save_data(videos)
            print(f"{user_name}, video '{removed['title']}' deleted successfully!")
        else:
            print("Invalid video number.")
    except ValueError:
        print("Invalid input.")

def clear_all_videos(videos, user_name):
    confirm = input("Are you sure you want to delete all videos? (y/n): ").lower()
    if confirm == 'y':
        videos.clear()
        save_data(videos)
        print(f"{user_name}, all videos deleted successfully!")
    else:
        print("Operation cancelled.")

def main():
    user_name = input("Welcome! Please enter your name: ").strip()
    if not user_name:
        user_name = "User"

    while True:
        clear_screen()
        print("*" * 70)
        print(f"\nHello, {user_name}! Welcome to the YouTube Manager.\n")
        print("*" * 70)

        videos = load_data()

        print(f"\n{user_name}, choose an option:")
        print("1. List all videos")
        print("2. Add a new video")
        print("3. Update a video")
        print("4. Delete a video")
        print("5. Clear all videos")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 6.")
            input("Press Enter to continue...")
            continue

        match choice:
            case 1:
                list_all_videos(videos)
                input("Press Enter to continue...")
            case 2:
                add_new_video(videos, user_name)
                input("Press Enter to continue...")
            case 3:
                update_video(videos, user_name)
                input("Press Enter to continue...")
            case 4:
                delete_video(videos, user_name)
                input("Press Enter to continue...")
            case 5:
                clear_all_videos(videos, user_name)
                input("Press Enter to continue...")
            case 6:
                print(f"Goodbye, {user_name}!")
                break
            case _:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    main()
