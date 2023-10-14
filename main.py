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
    log_msg = "Welcome in the Logger page"
    app.logger.info(log_msg)

    if request.method == 'POST':

        # Retreiived the text in the text box
        text_from_textbox = request.form['textbox']

        # Print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Web browser console : You are connected to the logger page');
            console.log('Text sent by the textbox : {text_from_textbox}');
        </script>
        """
    else:
        # Print a message in the browser console
        browser_log = """
        <script>
            console.log('Web browser console : You are connected to the logger page');
        </script>
        """

    # Text box
    textbox_form = """
    <form method="POST">
        <label for="textbox"><br><br>Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Submit">
    </form>
    """

    # Buttons for google request, google analytics request and cookies request
    button_msg = "<br>Google Requests :<br><br>"
    google_button = """
    <form method="GET" action="/google-request">
        <input type="submit" value="Google">
    </form>"""
    google_analytics_button = """<form method="GET" action="/google-analytics-request">
        <input type="submit" value="Google Analytics Dashboard">
    </form>
        """
    google_cookies_button = """<form method="GET" action="/google-cookies-request">
        <input type="submit" value="Google cookies">
    </form>
    """

    return log_msg + browser_log + textbox_form + button_msg + google_button + google_analytics_button + google_cookies_button

# Google request route
@app.route('/google-request', methods=['GET'])
def perform_google_request():
    # Question
    google_url = "https://www.google.com/"
    
    try:
        response = requests.get(google_url)
        response.raise_for_status()  
        return response.text
    # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics request: {str(e)}"
    
    
if __name__ == '__main__':
    app.run(debug=True)