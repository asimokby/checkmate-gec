# start a simple flask app
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_cors import CORS
import re
CLEANR = re.compile('<.*?>')
app = Flask(__name__)
CORS(app)

# making a global value so it doesn't reset every time
global value
value = None


@app.route('/', methods=['GET', 'POST'])
def index():
    # telling the program to use the global value instead of a local one
    global value
    if request.method == 'GET':
        if value:
            temp = value
            value = None
            return render_template('index.html', textValue=temp)
        else:
            return render_template('index.html')

    # if the method is POST, then it will get the value from the form
    else:
        data = request.form.get('mytextarea', 'no')
        # Cleaning the html tags from the data
        cleantext = re.sub(CLEANR, '', data)
        # setting the global value to the cleaned data
        value = checkText(cleantext.split())
        return redirect(url_for('index'))


def checkText(text):
    # checking if text is correct
    correctWords = ['this', 'hello', 'world']
    checkedWords = ''

    for word in text:
        if word in correctWords:
            checkedWords += word+' '

        else:
            checkedWords += ('<span style="color:red">' +
                             word +' ' + '</span>')
    return checkedWords


# IGNORE THIS PART

# # get data posted from API call
# @app.route('/api', methods=['GET', 'POST'])
# def api():
#     value = {}
#     if request.method == 'GET':
#         return value
#     if request.method == 'POST':
#         data = request
#         print(data.get_json())
#         # return data as a json
#         return {1:"hello"}
if __name__ == '__main__':
    app.run(debug=True)
