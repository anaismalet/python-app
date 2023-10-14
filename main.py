from flask import Flask, request
import logging
import requests

# Flask app
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def hello_world():
    # Adding a google tag for google analysis
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-LGCXZQVT0R"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-LGCXZQVT0R');
    </script>
    """
    # Return the tag and a print "Hello world"
    return prefix_google + "Hello World"

# Route to logger page
@app.route("/logger", methods=['GET', 'POST'])
def log():
    # Print a message in Python
    log_msg = "Logger page"
    app.logger.info(log_msg)

    if request.method == 'POST':
        # Retreiived the text in the text box
        text_from_textbox = request.form['textbox']

        # Print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
            console.log('Texte de la boîte de texte : {text_from_textbox}');
        </script>
        """
    else:
        # Print a message in the browser console
        browser_log = """
        <script>
            console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
        </script>
        """

    # Formulaire HTML avec une boîte de texte
    textbox_form = """
    <form method="POST">
        <label for="textbox">Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Soumettre">
    </form>
    """

    return log_msg + browser_log + textbox_form

@app.route('/google-request', methods=['GET'])
def google_request():
    # Render a form with a button to make the Google request
    return """
    <form method="GET" action="/google-analytics-request">
        <input type="submit" value="Display Google Analytics Dashboard">
    </form>
    <form method="GET" action="/google-cookies-request">
        <input type="submit" value="Display Cookies">
    </form>
    """


if __name__ == '__main__':
    app.run(debug=True)