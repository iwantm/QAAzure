from flask import Flask, render_template
from os import getenv
import uuid, json, requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


app = Flask(__name__)

app.config['SECRET_KEY']=getenv('SECRET_KEY')

langs = requests.get('https://api.cognitive.microsofttranslator.com/languages?api-version=3.0')
langs = langs.json()
languages = []
for lang in langs['translation']:
    languages.append((lang,langs['translation'][lang]['nativeName']))

class TranslateForm(FlaskForm):

    sentence = StringField('Enter Some Text')
    language = SelectField('Language',
        choices=languages)
    submit = SubmitField('Translate')

@app.route('/', methods=['GET', 'POST'])
def translate():
    form = TranslateForm()
    response = ""
    if form.validate_on_submit():
        subscription_key = getenv('TRANSLATOR_TEXT_SUBSCRIPTION_KEY')
        endpoint = getenv('TRANSLATOR_TEXT_ENDPOINT')
        addition = "translate?api-version=3.0&to="
        headers = {
        'Ocp-Apim-Subscription-Key':subscription_key,
        'Ocp-Apim-Subscription-Region':'global',
        'Content-Type':'application/json'
        }
        body = [{
        'Text': form.sentence.data
        }]
        constructed_url = endpoint + addition + form.language.data
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        response = response[0]['translations'][0]['text']
    return render_template('index.html', form=form, translation=response)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
