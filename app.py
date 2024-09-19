from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import google.generativeai as genai


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



@app.route("/", methods=['GET', 'POST'])
def load():
    return render_template("loader.html")

@app.route('/home')
def index():
    return render_template('index.html')


data= []

# Endpoint to handle text and store it in the database
@app.route("/gemini", methods=['GET', 'POST'])
def text():

    data = session.get('data', [])

    if request.method == "POST":
        input_text = request.form.get("text")

        if input_text:
            # Using generative AI model to generate content
            model = genai.GenerativeModel(model_name="gemini-pro")
            response = model.generate_content(input_text)
            text_result = response.text
            
            data.append({'input': input_text, 'result': text_result})
            session['data'] = data

            return redirect(url_for('text'))
        
        else:
            flash("Please provide a valid input!", "error")

    return render_template("gemini.html", data=data[::-1])


@app.route("/logout")
def logout():
    session.pop('data', None)
    return redirect(url_for('load'))

 
if __name__ == '__main__':
    app.run(debug=True)