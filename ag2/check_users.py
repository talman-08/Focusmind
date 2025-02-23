import sqlite3

db_path = "/Users/wissamfarhat/Desktop/Myproject/users.db"  # Ensure this is correct
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the users table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
table_exists = cursor.fetchone()

if not table_exists:
    print("❌ The 'users' table does not exist.")
    conn.close()
    exit()

# Check if any users exist
cursor.execute("SELECT username, password FROM users")
users = cursor.fetchall()

if not users:
    print("⚠️ No users found. Adding a test user...")
    cursor.execute("INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)", 
                   ("testuser", "password123", "test@example.com", "Test User"))
    conn.commit()
    print("✅ Test user added successfully!")
else:
    print("📌 Registered Users:")
    for user in users:
        print(f"Username: {user[0]}, Password: {user[1]}")

conn.close()
