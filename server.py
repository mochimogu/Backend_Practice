from flask import Flask, render_template


app = Flask(__name__, static_folder='templates')



@app.route('/')
def start():
    return render_template("app.html")



if __name__ == "__main__":
    app.run(debug=True)