# start a simple flask app
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_cors import CORS
import re
import nltk
from happytransformer import HappyTextToText, TTSettings

nltk.download('punkt')

CLEANR = re.compile('<.*?>')
app = Flask(__name__)
CORS(app)

# making a global value so it doesn't reset every time
global value
value = None


happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)


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
        output = correct_errors(cleantext)
        value = sendText(output)
        return redirect(url_for('index'))


def correct_errors(text):
    """ 
        Returns a list of tuples containing: 
            0th index: the sentence.
            1th index: the indexes where the model detected an error. 
            2th index: the corrected sentence. 
    """
    output = []
    sent_text = nltk.sent_tokenize(text)
    for sent in sent_text:
        result = happy_tt.generate_text(f"grammar: {sent}", args=args)
        bad_idxs = [idx for idx, elem in enumerate(result.text.split()) if elem != sent.split()[idx]]
        output.append([sent, bad_idxs, result.text])

    return output

def sendText(text):
    # checking if text is correct
    checkedWords = ''

    for sentence in text:
        if(len(sentence[1]) == 0):
            checkedWords += sentence[0] + ' '
        else:
            for idx, word in enumerate(sentence[0].split()):
                if idx in sentence[1]:
                    checkedWords += ('<del><span class="wrong" style="color:red">' +
                                     word +'</del> ' + '</span>' +'<span class="" style="color: green">'+ sentence[2].split()[idx] + ' '+'</span>')
                else:
                    checkedWords += word + ' '
    return checkedWords
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
