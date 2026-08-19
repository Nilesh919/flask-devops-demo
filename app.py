from flask import Flask, request, render_template

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "admin123"


@app.route("/", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            message = "Login successful!"
        else:
            message = "Invalid username or password!"

    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
