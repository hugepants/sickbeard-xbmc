import xbmcaddon
import os
import urllib
import urllib2
import sys
import xbmcgui

def createURL(ip, port, custom_url):
    if custom_url != "":
        return custom_url
    if str(ip) == "" or str(port) == "":
        displayError("1")
    else:
        return "http://"+str(ip)+":"+str(port)
    
# Hackish... not sure if there is a better way to get the API key
# Parses the HTML of the General page and pulls the API key
def GetAPIKey(ip, port, username, password, custom_url):
    # Get API key from Sickbeark
    base_url = createURL(ip, port, custom_url)
    if username and password:
        try:
            password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            url = base_url + '/config/general/'
            password_manager.add_password(None, url, username, password)
            authhandler = urllib2.HTTPBasicAuthHandler(password_manager)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            result = result.readlines()
        except urllib2.HTTPError:
            displayError("2")
        except urllib2.URLError:
            displayError("3")
    else:    
        try:
            html=urllib.urlopen(base_url+'/config/general/')
            result=html.readlines()
            html.close()
        except:
            displayError("3")

    api_line = ""
    for line in result:
      if "name=\"use_api\"" in str(line):
        if "checked=\"checked\"" not in str(line):
            displayError("4")
      if "id=\"api_key\"" in str(line):
        api_line = line
    api_index = api_line.index("value=\"")+7
    APIKey = api_line[api_index:api_index+32]
    if APIKey == "":
        displayError("4")
    return APIKey

# Set constants
__addon__ = xbmcaddon.Addon(id='plugin.program.sickbeard')
__ip__ = __addon__.getSetting('Sickbeard IP')
__port__= __addon__.getSetting('Sickbeard Port')
__username__ = __addon__.getSetting('Sickbeard Username')
__password__= __addon__.getSetting('Sickbeard Password')
__url_bool__= __addon__.getSetting('CustomURL')
if __url_bool__ == "true":
    __custom_url__= __addon__.getSetting('Sickbeard URL')
else:
    __custom_url__= ""

# Show error pop up then exit plugin
def messageWindow(header, message):
    dialog = xbmcgui.Dialog()
    dialog.ok(header, message)

# Show error pop up then exit plugin
def errorWindow(header, message):
    dialog = xbmcgui.Dialog()
    dialog.ok(header, message)
    sys.exit()

# Display the correct error message based on error code
def displayError(error_code):
    if error_code == "1":
        errorWindow("Sickbeard Error", "Must configure IP and port settings before use")
    elif error_code == "2":
        errorWindow("Sickbeard Error", "Invalid username or password.")
    elif error_code == "3":
        errorWindow("Sickbeard Error", "Unable to connect to Sickbeard.\nCheck Sickbeard IP and port.")
    elif error_code == "4":
        errorWindow("Sickbeard Error", "Unable to retrieve API key.\nCheck API is enabled under general settings.")


__APIKey__ = GetAPIKey(__ip__, __port__, __username__,__password__, __custom_url__)
__url__='http://'+__ip__+':'+__port__+'/api/'+__APIKey__+'/'
