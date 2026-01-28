import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

conn = sqlite3.connect("youtube_videos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    time TEXT NOT NULL,
    description TEXT
);
""")
conn.commit()

cursor.execute("PRAGMA table_info(videos)")
columns = [col[1] for col in cursor.fetchall()]
if "description" not in columns:
    cursor.execute("ALTER TABLE videos ADD COLUMN description TEXT")
    conn.commit()

def load_data():
    cursor.execute("SELECT * FROM videos")
    rows = cursor.fetchall()
    videos = []
    for row in rows:
        videos.append({
            "id": row[0],
            "title": row[1],
            "time": row[2],
            "description": row[3] if len(row) > 3 else ""
        })
    return videos

def save_data(videos):
    cursor.execute("DELETE FROM videos")
    for video in videos:
        cursor.execute(
            "INSERT INTO videos (id, name, time, description) VALUES (?, ?, ?, ?)",
            (video["id"], video["title"], video["time"], video["description"])
        )
    conn.commit()

def list_all_videos(videos):
    if not videos:
        print("No videos found.")
        return
    for i, video in enumerate(videos, start=1):
        print("\n")
        print("*" * 70)
        print(f"{i}. Title      : {video['title']}")
        print(f"   Time       : {video['time']}")
        print(f"   Description: {video['description']}")
        print("*" * 70)
        print("\n")

def add_new_video(videos, user_name):
    title = input("Enter video title: ")
    time = input("Enter video time: ")
    description = input("Enter video description: ")
    next_id = max([v["id"] for v in videos], default=0) + 1
    videos.append({
        "id": next_id,
        "title": title,
        "time": time,
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
            videos[index]["title"] = input("Enter new title: ")
            videos[index]["time"] = input("Enter new time: ")
            videos[index]["description"] = input("Enter new description: ")
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
    if confirm == "y":
        videos.clear()
        save_data(videos)
        print(f"{user_name}, All videos deleted successfully!")
    else:
        print("Operation cancelled.")

def main():
    clear_screen()
    print("*" * 70)
    user_name = input("Welcome! Please enter your name: ").strip()
    if not user_name:
        user_name = "User"
    print(f"\nHello, {user_name}! Welcome to the YouTube Manager.\n")
    print("*" * 70)

    while True:
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
    conn.close()
