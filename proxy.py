import webapp
import urllib
import string


class proxy(webapp.webApp):

    myUrl = "http://localhost:3333"
    cacheDict = {}
    head1Dict = {}
    head3Dict = {}

    def putMenu(self, html, url):
        posTagBody = string.find(html, "<body")
        posTagBody = string.find(html, ">", posTagBody)
        html1 = html[0: posTagBody + 1]
        html2 = html[posTagBody + 1:]
        original = '<a href="http://' + url + '">Original</a>'
        refresh = '<a href="' + self.myUrl + "/" + url + '">Refresh</a>'
        cache = '<a href="' + self.myUrl + '/cache/' + url + '">Cache</a>'
        head1 = '<a href="' + self.myUrl + '/head1/' + url + '">Head1</a>'
        head2 = '<a href="' + self.myUrl + '/head2/' + url + '">Head2</a>'
        head3 = '<a href="' + self.myUrl + '/head3/' + url + '">Head3</a>'
        head4 = '<a href="' + self.myUrl + '/head4/' + url + '">Head4</a>'
        return html1 + " " + original + " " + refresh + " " + cache + " " + \
            head1 + " " + head2 + " " + head3 + " " + head4 + " " + html2

    def getcache(self, url):
        try:
            httpBody = self.cacheDict[url]
            httpCode = "200 OK"
        except KeyError:
            httpCode = "404 Resource Not Available"
            httpBody = "Error: Doesn't exist that url in cache"
        return (httpBody, httpCode)

    def gethead1(self, url):
        try:
            headers = self.head1Dict[url]
            httpBody = "<html><p>Client -> Proxy:</p><p>" + \
                headers + "</p></html>"
            httpCode = "200 OK"
        except KeyError:
            httpCode = "404 Resource Not Available"
            httpBody = "Error: Doesn't exist that url in headers"
        return (httpBody, httpCode)

    def gethead3(self, url):
        try:
            headers = self.head3Dict[url]
            httpBody = "<html><p>Real server -> Proxy:</p><p>" + \
                headers + "</p></html>"
            httpCode = "200 OK"
        except KeyError:
            httpCode = "404 Resource Not Available"
            httpBody = "Error: Doesn't exist that url in headers"
        return (httpBody, httpCode)

    def parse(self, request):
        resources = request.split()[1][1:]
        resList = resources.split("/", 1)
        headers = request.split("\r\n\r\n")[0]
        return (resList, headers)

    def process(self, parsedRequest):
        (resources, headers) = parsedRequest
        if len(resources) == 1:
            url = resources[0]
            try:
                file = urllib.urlopen("http://" + url)
                html = file.read()
                html = self.putMenu(html, url)
                httpCode = "200 OK"
                httpBody = html
                self.cacheDict[url] = html
                self.head1Dict[url] = headers
                self.head3Dict[url] = str(file.info())
            except IOError:
                httpCode = "404 Resource Not Available"
                httpBody = "Error: could not connect"
        elif resources[0] == "cache":
            url = resources[1]
            (httpBody, httpCode) = self.getcache(url)
        elif resources[0] == "head1":
            url = resources[1]
            (httpBody, httpCode) = self.gethead1(url)
        elif resources[0] == "head2":
            httpCode = "200 OK"
            httpBody = "<html><p>Proxy -> Real server:</p></html>"
        elif resources[0] == "head3":
            url = resources[1]
            (httpBody, httpCode) = self.gethead3(url)
        elif resources[0] == "head4":
            httpCode = "200 OK"
            httpBody = "<html><p>Proxy -> Client:</p></html>"
        else:
            httpCode = "404 Resource Not Available"
            httpBody = "Error: resource not available "

        return (httpCode, httpBody)

if __name__ == "__main__":
    try:
        testWebApp = proxy("localhost", 3333)
    except KeyboardInterrupt:
        print "\nExit\n"
