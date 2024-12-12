from flask import Flask, request, render_template_string, redirect, url_for, flash
from instagrapi import Client

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template for the web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Nickname Changer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #fff;
        }
        .container {
            background-color: #333;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #fff;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            color: #fff;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus {
            outline: none;
            border-color: #ff7e5f;
            box-shadow: 0 0 5px rgba(255, 126, 95, 0.5);
        }
        button {
            background-color: #ff7e5f;
            color: #fff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #feb47b;
        }
        .message {
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Nickname Changer</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Target Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group chat ID" required>

            <label for="nickname">Nickname for All Members:</label>
            <input type="text" id="nickname" name="nickname" placeholder="Enter the new nickname" required>

            <button type="submit">Change Nicknames</button>
        </form>
    </div>
</body>
</html>
'''

# Flask route for the web page
@app.route("/", methods=["GET", "POST"])
def change_nicknames():
    if request.method == "POST":
        # Retrieve form data
        username = request.form["username"]
        password = request.form["password"]
        group_id = request.form["group_id"]
        nickname = request.form["nickname"]

        try:
            # Log in to Instagram
            cl = Client()
            flash("[INFO] Logging in...")
            cl.login(username, password)
            flash("[SUCCESS] Logged in!")

            # Retrieve group chat information
            group_info = cl.direct_thread(group_id)
            members = group_info.users

            # Change nicknames for all members
            for member in members:
                user_id = member.pk
                cl.direct_change_thread_nickname(group_id, nickname, user_id)
                print(f"Nickname changed for {member.username} to {nickname}")
            
            flash("Nicknames updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("change_nicknames"))

    # Render HTML template
    return render_template_string(HTML_TEMPLATE)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
