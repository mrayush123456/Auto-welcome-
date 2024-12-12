from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time

# Flask app setup
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Welcomer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin-top: 10px;
            font-weight: bold;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Group Welcomer</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>
            
            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
            
            <label for="group_id">Target Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group chat ID" required>
            
            <label for="welcome_message">Welcome Message:</label>
            <input type="text" id="welcome_message" name="welcome_message" placeholder="Enter welcome message" required>
            
            <button type="submit">Send Welcome</button>
        </form>
    </div>
</body>
</html>
'''

# Route for the form
@app.route("/", methods=["GET", "POST"])
def send_welcome():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            welcome_message = request.form["welcome_message"]

            # Log in to Instagram
            cl = Client()
            flash("Logging into Instagram...", "info")
            cl.login(username, password)
            flash("Login successful!", "success")

            # Fetch group members
            group_info = cl.direct_thread(group_id)
            member_usernames = [user.username for user in group_info.users]

            # Create a message mentioning all members
            mentions = " ".join([f"@{user}" for user in member_usernames])
            final_message = f"{welcome_message}\n{mentions}"

            # Send the message
            cl.direct_send(final_message, thread_ids=[group_id])
            flash("Welcome message sent successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for("send_welcome"))

    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
            
