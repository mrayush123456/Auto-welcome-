from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import threading

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template for the Web Page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Auto-Welcome</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #ffffff;
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus {
            outline: none;
            border: 2px solid #ffffff;
        }
        button {
            background-color: #6a11cb;
            color: #ffffff;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background-color: #2575fc;
        }
        .info {
            font-size: 12px;
            color: #cccccc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Auto-Welcome</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Target Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group chat ID" required>

            <label for="welcome_message">Welcome Message:</label>
            <input type="text" id="welcome_message" name="welcome_message" placeholder="Enter the welcome message" required>

            <button type="submit">Start Welcoming</button>
        </form>
    </div>
</body>
</html>
'''

# Function to monitor the group chat and send welcome messages
def monitor_group(cl, group_id, welcome_message):
    print("[INFO] Monitoring group chat for new members...")
    previous_members = set()

    while True:
        try:
            # Fetch group chat details
            group_info = cl.direct_thread(group_id)
            current_members = {member.pk for member in group_info.users}

            # Identify new members
            new_members = current_members - previous_members
            for new_member in new_members:
                print(f"[INFO] New member detected: {new_member}")
                cl.direct_send(welcome_message, thread_ids=[group_id])
                print(f"[SUCCESS] Welcome message sent to {new_member}")

            # Update the previous members list
            previous_members = current_members

        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")

# Flask Route for Handling Form Submission
@app.route("/", methods=["GET", "POST"])
def instagram_auto_welcome():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            welcome_message = request.form["welcome_message"]

            # Initialize Instagram client
            cl = Client()
            print("[INFO] Logging into Instagram...")
            cl.login(username, password)
            print("[SUCCESS] Logged in!")

            # Start monitoring group chat in a separate thread
            threading.Thread(target=monitor_group, args=(cl, group_id, welcome_message), daemon=True).start()

            flash("Auto-welcome process started!", "success")
            return redirect(url_for("instagram_auto_welcome"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("instagram_auto_welcome"))

    # Render the HTML form
    return render_template_string(HTML_TEMPLATE)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
