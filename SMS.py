"""
API SMS FOR OUR SELF PHONES... To know when the script is finished
"""

import urllib.request
import urllib.parse
import config as conf


def sendSMS(message):
    data = urllib.parse.urlencode({'apikey': conf.sms_api_key, 'numbers': conf.sms_numbers,
                                   'message': message, 'sender': "GoG Scrapper"})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)
