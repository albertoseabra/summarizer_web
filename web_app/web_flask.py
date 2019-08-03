from flask import Flask, jsonify, make_response, render_template, request, current_app
import pymongo

from summarizer import Summarizer

app = Flask(__name__)


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
    url = ""
    text = ""
    summary = []
    key_words = []
    summary_method = "textrank_tfidf"
    if request.method == "POST":
        # get url that the user has entered
        url = request.form['url']
        text = request.form["message"]
        summary_method = request.form["summary_method"]
        if url:
            results = "detected URL: {}".format(url)
            summarizer = Summarizer(url=url)
            if summary_method == "textrank_tfidf":
                results = summarizer.textrank_summary()
            elif summary_method == "embeddings":
                results = summarizer.doc_embedding_summary()
            elif summary_method == "clustering":
                results = summarizer.clustering_summary()

        if text:
            results += "detected text: {}".format(text)
        if (not url) & (not text):
            errors.append("You need to provide an URL or a text to summarize")

    return render_template('index.html', errors=errors, results=results, url=url, text=text)


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
    app.run(host="0.0.0.0", debug=True)
