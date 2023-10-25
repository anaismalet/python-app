from flask import Flask, request, render_template, jsonify
import logging
import requests
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta import RunReportRequest
#from pytrends.request import TrendReq

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
    log_msg = "ANAÏS MALET, LAB 2 et 3 DIGITAL TRACES<br><br>Welcome in the Logger page "
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
        <label for="textbox"><br><br>Write something you want to display in the console :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Submit">
    </form>
    """

    # Buttons for google request, google analytics request and cookies request
    button_msg = "<br>Google Requests :<br><br>"
    google_button = """
    Let's do a goole research :
    <form method="GET" action="/google-request">
        <input type="submit" value="Google">
    </form>"""
    google_analytics_button = """Let's go to Google Analytics : <form method="GET" action="/google-analytics-request">
        <input type="submit" value="Google Analytics Dashboard">
    </form>
        """
    google_cookies_button = """Let's get the cookies informations from google analytics : <form method="GET" action="/google-cookies-request">
        <input type="submit" value="Google cookies">
    </form>
    """
    google_analytics_api = """Let's get the visitors number on this website from Google Analytics API : <form method="GET" action="/api-google-analytics-data">
        <input type="submit" value="Google Analytics API">
    </form>
        """
    
    google_trend_button = """Let's display the trend comparison time serie between France and Spain from Google trend : <form method="GET" action="/chart-data">
        <input type="submit" value="Google Trend">
    </form>
        """

    return log_msg + browser_log + textbox_form + button_msg + google_button + google_analytics_button + google_cookies_button + google_analytics_api + google_trend_button

# Google request
@app.route('/google-request', methods=['GET'])
def google_request():
    # Question
    google_url = "https://www.google.com/"
    
    try:
        response = requests.get(google_url)
        response.raise_for_status()  
        return response.text
    # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return f"Error making Google request: {str(e)}"
    
# Google analytics request
@app.route('/google-analytics-request', methods=['GET'])
def google_analytics_request():
    # Question
    google_analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        # Return response from get request
        return response.text
   
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics request: {str(e)}"

# Google cookies request
@app.route('/google-cookies-request', methods=['GET'])
def google_cookies_request():

    google_analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status() # Raise an exception for HTTP errors

        # Retrieve cookies of the response
        cookies = response.cookies

        # Send cookies to the template for display
        return render_template('cookies.html', cookies=cookies)
    
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics Cookies request: {str(e)}"
    
# Fetch data from Google analytics api
@app.route('/api-google-analytics-data', methods=['GET'])
def api_google_analytics_data():

    # Set the path to the Google Cloud credentials file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'lab-2-data-traces-3cceca2c0880.json'
    # Define Google Analytics property ID, and a period of time with starting date and ending date
    GA_property_ID = '407449812'
    starting_date = "28daysAgo"
    ending_date = "yesterday"

    # Initialize a client for the Google Analytics Data API
    client = BetaAnalyticsDataClient()
    
    # Function that gets the number of visitors
    def get_visitors_number(client, property_id):
        # Define the request to retrieve active users metric
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)
        # return active_users_metric
        return response

    # Get the visitor number using the function
    response = get_visitors_number(client, GA_property_ID)

    # Check if there's a valid response with data
    if response and response.row_count > 0:
        # Extract the value of the active users metric from the response
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  # Handle the case where there is no data

    return f'Active users of your app : {metric_value}'

# It should works but my computer does not handle pytrends importation so I had to hide "import pytrend" in commentary
@app.route('/chart-data')
def chart_data():
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = ["France", "Spain"]
    pytrends.build_payload(keywords, timeframe='today 12-m', geo='US')
    interest_over_time_df = pytrends.interest_over_time()

    data = {
        'dates': interest_over_time_df.index.strftime('%Y-%m-%d').tolist(),
        'France': interest_over_time_df['France'].tolist(),
        'Spain': interest_over_time_df['Spain'].tolist()
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)