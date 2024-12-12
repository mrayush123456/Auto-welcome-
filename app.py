from flask import Flask, request, render_template_string, redirect, flash
from instagrapi import Client
import time

# Flask app initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Nickname Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: white;
            text-align: center;
            padding: 50px;
        }
        .container {
            max-width: 400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        input {
            background: rgba(255, 255, 255, 0.2);
            color: white;
        }
        button {
            background: #4caf50;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Nickname Bot</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Instagram Username" required>
            <input type="password" name="password" placeholder="Instagram Password" required>
            <input type="text" name="group_id" placeholder="Group Chat ID" required>
            <input type="text" name="nickname" placeholder="New Nickname for Members" required>
            <button type="submit">Update Nicknames</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def change_nicknames():
    if request.method == "POST":
        # Fetch form data
        username = request.form["username"]
        password = request.form["password"]
        group_id = request.form["group_id"]
        nickname = request.form["nickname"]

        try:
            # Log in to Instagram
            client = Client()
            client.login(username, password)
            flash("Logged in successfully!", "success")

            # Fetch the group chat
            group = client.direct_threads(thread_ids=[group_id])[0]
            user_ids = [user.pk for user in group.users]

            # Change nickname for each member
            for user_id in user_ids:
                client.direct_thread_update_user_nickname(
                    thread_id=group_id, 
                    user_id=user_id, 
                    nickname=nickname
                )
                flash(f"Changed nickname for user {user_id} to {nickname}", "success")
                time.sleep(2)  # Avoid rate limits

            flash("Nicknames updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect("/")

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
