from flask import Flask, request, render_template, redirect
 
import import_session

app = Flask(__name__)

@app.route("/")
def home():
    """Home page; student and project lists (linked)."""


    return "hi"

if __name__ == "__main__":
    import_session.connect_to_db(app)
    app.run(debug=True)