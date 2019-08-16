from flask import Flask, jsonify, make_response, render_template, request, current_app, redirect, url_for
import pickle
from mongoengine import connect

from summarizer import Summarizer
import config_file as config_file
import text_save as text_save

app = Flask(__name__)
app.config.from_object(config_file.DevelopmentConfig())

connect(app.config["MONGODB_DATABASE"],
        host=app.config["MONGODB_IP"])

tfidf_tokenizer = pickle.load(open(app.config["TFIDF_TOKENIZER"], "rb"))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    errors = []
    results = ""
    summary = []
    key_words = []
    summary_method = "textrank_tfidf"
    if request.method == "POST":
        # get url that the user has entered
        url = request.form['url']
        text = request.form["message"]
        summary_method = request.form["summary_method"]
        try:
            number_sentences = int(request.form["number_sentences"])
        except ValueError:
            number_sentences = 3
        if (not url) & (not text):
            errors.append("You need to provide an URL or a text to summarize")
            return render_template('index.html', errors=errors)

        else:
            if url:
                # results = "detected URL: {}".format(url)
                summarizer = Summarizer(tfidf_tokenizer=tfidf_tokenizer, url=url)
            elif text:
                # results += "detected text: {}".format(text)
                summarizer = Summarizer(tfidf_tokenizer=tfidf_tokenizer, text=text)

            if number_sentences > len(summarizer.sentences):
                errors.append("You are asking for a summary of {} sentences but the original text only has {} "
                              "sentences".format(number_sentences, len(summarizer.sentences)))
                return render_template('index.html', errors=errors)

            if summary_method == "textrank_tfidf":
                summary = summarizer.textrank_summary(number_sentences)
            elif summary_method == "embeddings":
                summary = summarizer.doc_embedding_summary(number_sentences)
            elif summary_method == "clustering":
                summary = summarizer.clustering_summary(number_sentences)

            key_words = summarizer.key_words(5)

            rating = 5
            text_to_store = text_save.TextToStore(text=summarizer.text,
                                                  title=summarizer.title,
                                                  url=summarizer.url,
                                                  source=summarizer.source,
                                                  summary=text_save.Summary(text=summary,
                                                                            method=summary_method,
                                                                            size=number_sentences,
                                                                            rating=rating))

            text_to_store.save()

            return render_template("summary_result.html", title=summarizer.title, results=summary, key_words=key_words)

    return render_template('index.html', errors=errors)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # recaptcha = current_app.config['RECAPTCHA_SITE_KEY']
    email_sent = False

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        message = request.form['message']
        # recaptcha_response = request.form['g-recaptcha-response']

        # send_email(app, to=current_app.config['ADMIN_EMAIL'], subject="Contact Form Flask Shop",
        #            body=email + " " + name + " " + message)

        email_sent = True

    return render_template("contact.html", email_sent=email_sent)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# @app.errorhandler(404)
# def not_found(error):
#     """ error handler """
#     # LOG.error(error)
#     return make_response(jsonify({'error': 'Not found'}), 404)
# @app.route('/summarizer')
# def about():
#   return render_template('about.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     int_features = [int(x) for x in request.form.values()]
#     final_features = [np.array(int_features)]
#     prediction = model.predict(final_features)
#
#     output = round(prediction[0], 2)
#
#     return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))

#
# @app.route('/predict_api',methods=['POST'])
# def predict_api():
#     '''
#     For direct API calls trought request
#     '''
#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])
#
#     output = prediction[0]
#     return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
