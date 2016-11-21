from flask import Flask, render_template

app = Flask(__name__)


@app.route('/comments')
def comments():
    comments = ['comment 1', 'comment 2', 'comment 3']
    return render_template('comments.html', comments=comments)


if __name__ == "__main__":
    app.run(debug=True)