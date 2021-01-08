import smtplib
import ssl
import yfinance as yf
import json

stocks_to_be_notified = {}

# JSON file holds all the stocks and whether or not we have already sent a
# notification or not. If a notification has already been sent (True), no need
# to resend.
with open("data.json") as json_file:
    data = json.load(json_file)

# Stocks Being Watched: Air Canada
# 1) Air Canada
ac = yf.Ticker("AC.TO")
ac_bid = ac.info['bid']
if ac_bid < 35 and data["Air Canada"] == "False":
    stocks_to_be_notified["Air Canada"] = ac_bid

# Now, we need to change the json file so that all the stocks in
# stocks_to_be_notified are "True", since we are sending the email.
if stocks_to_be_notified:
    with open("scratch.json", "w") as json_file:
        for stock_name in stocks_to_be_notified:
            data[stock_name] = "True"
            json.dump(data, json_file)

    # We can close the JSON file now.
    json_file.close()

    # Send email if there are any stocks to be notified
    list = ""
    for stock in stocks_to_be_notified:
        list += "\n\t" + stock + ": " + str(stocks_to_be_notified[stock]) + "\n"
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "tanmayshahdev@gmail.com"  # Enter your address
    receiver_email = "tanmayshahdev@gmail.com"  # Enter receiver address
    password = input("Please enter your email password: ")
    message = """
    Here are some stocks that have met your requirements:
    """ + list

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
