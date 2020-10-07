from functions import process
from flask import Flask
from flask import render_template
from flask import request

# HTML templates called by the Flask API are located at
# ../templates
app = Flask(__name__, template_folder="../templates/")


@app.route('/ranked_text', methods=['GET', 'POST'])
def main():
    """Display HTML template and retrieve user input from locally hosted
    site, before disaggregating values at arguments for process() function"""
    url = request.args.get('url')
    text_type = request.args.get('text_type')
    choice = f"{url}, {text_type}"
    choice_list = [x.split() for x in choice.split(',')]

    if not url:
        print("ERROR: No URL entered")
    else:
        process(str(choice_list[0][0]), str(choice_list[1][0]))

    return render_template("form.html", choice=choice)


if __name__ == "__main__":
    app.run()
