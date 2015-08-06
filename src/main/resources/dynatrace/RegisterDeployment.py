#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, string
import datetime

STATUS_SUCCESS = 201
STATUS_FORBIDDEN = 403

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)
# watch for encoding problems
if not message:
    message = "Deployment"
if not description:
    description = "Triggered through XLRelease"
if not severity:
    severity = "informational"
if not start:
    start = datetime.datetime.now().isoformat()
if not end:
    end = start

body = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><incident><message>%s</message><description>%s</description><severity>%s</severity><start>%s</start><end>%s</end></incident>" % (message,description,severity,start,end)
print "body: ", body
response = connection.post("/rest/management/profiles/%s/incidentrules/Deployment/incidents" % profile, body, contentType="application/xml")

if response.status == STATUS_SUCCESS:
    print "successfully set the deployment incident"
else:
    print "Failed to set deployment incident %s.\n" % response.response
    response.errorDump()
    sys.exit(1)
