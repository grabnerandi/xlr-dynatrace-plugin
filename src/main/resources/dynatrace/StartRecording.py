#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, string
import com.xhaus.jyson.JysonCodec as json
from com.xebialabs.xlrelease.plugin.webhook import XmlPathResult

STATUS_SUCCESS = 200
STATUS_FORBIDDEN = 403

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)
body = ""
# watch for encoding problems
if presentableName:
    body += "presentableName=" + presentableName
if description:
    body += "&description=" + description

response = connection.post("/rest/management/profiles/%s/startrecording" % profile, body, contentType="text/xml")


if response.status == STATUS_SUCCESS:
    sessionName = XmlPathResult(response.response, "/result/@value").get()
    print "Started Recording of Session %s via Dynatrace server at %s.\n" % (sessionName, serverUrl)
elif response.status == STATUS_FORBIDDEN:
    errorText = XmlPathResult(response.response, "/error/@reason").get()
    print "Started Recording failed: %s\n" % (errorText)   
    response.errorDump()	
else:
    print "Failed to start recording via Dynatrace server at %s.\n" % serverUrl
    response.errorDump()
    sys.exit(1)
