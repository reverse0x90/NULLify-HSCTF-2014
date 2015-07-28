#!/usr/bin/python

# Check User Agent utility used by the template to show the appropriate message.    
def checkUserAgent(userAgentString):
    if 'MSIE' in userAgentString:
        isIE = 'True'
    elif 'Trident' in userAgentString:
        isIE = 'True'
    else:
        isIE = 'False'

    return isIE
