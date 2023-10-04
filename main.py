

from flask import Flask
import logging

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

@app.route("/logger")
def logger():
    
    # print a message on the logger page
    log = "Logger page"

    # print a message in Python, check in deta micro
    app.logger.info("Message python : connexion page logger")

    # print a message in the browser console, check in console browser
    browser_log = """
    <script>
        console.log('Message in browser : connexion à la page Logger');
    </script>
    """

    return  browser_log + log

