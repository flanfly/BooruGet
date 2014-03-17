"""
Frank Hrach
Gelbooru.py
Sun Mar  9 22:29:53 EDT 2014
"""

import Booru

import httplib2
import xml.etree.ElementTree as ET

import time


class GelbooruDownloader(Booru):

    URL = "http://gelbooru.com/index.php?page=dapi&s=post&q=index"
    NUMBER_PER_PAGE = 100

    searchString = ""
    targetWidth = -1
    targetHeight = -1

    pageNum = 0
    numberOfPages = 1000

    verbose = False

    def __init__(self, searchString, targetWidth, targetHeight, error):
        self.searchString = searchString
        self.targetWidth = targetWidth
        self.error = error

    def getResults(self):
        pass

    def connect(self):
        if self.verbose:
            print "Gelbooru: Reqesting page"
        try:
            connection = httplib2.Http(".cache")
            res, content = connection.request(
                self.URL + "&tags=" + self.searchString + "&pid=" +
                str(self.pageNum) + "&limit=" + str(self.NUMBER_OF_PAGES))
            if self.verbose:
                print "\tResults recieved"
            if not (res.status == 200):
                if self.verbose:
                    print "\tResponse was not 200 (" + res.status + ")"
                else:
                    print "Error with search, trying again"
                time.sleep(5000)
                self.connect()
            if len(content) >= 0:
                if self.verbose:
                    print "\tResponse was 200"
                    print "Done"
                return ET.fromstring(content)
            else:
                return None
        except (httplib2.ServerNotFoundError):
            print "Could not contact server at gelbooru.com"
            print "Retrying in 30 seconds"
            time.sleep(30)
            self.connect()
        return None

        def download():
            root = connect(url, 1, numPerPage, searchString)
            numberOfPages = int(
                math.ceil(int(root.attrib["count"]) / float(len(root))))

            time.sleep(0.2)
            for i in range(1, numPages + 1):

                # if call to exit is found, break out of this loop now
                if exitapp:
                    break

                root = getResultsXML(url, i, numPerPage, searchString)

                if arguments.verbose:
                    print "Gelbooru: current page: " + str(i) + " (" + \
                        str(i * numPerPage) + ") out of " + str(numPages) + \
                        " pages(" + root.attrib["count"] + ")"

                try:
                    for child in root:
                        #TODO check to make sure result has data
                        image = {}
                        image["md5"] = child.attrib["md5"]
                        image["image_height"] = int(child.attrib["height"])
                        image["image_width"] = int(child.attrib["width"])
                        image["rating"] = child.attrib["rating"]
                        image["tag_string"] = child.attrib["tags"]
                        image["file_ext"] = \
                            child.attrib["file_url"].split(".")[3]

                        if filterResult(image, tWidth, tHeight, error):
                            while numthreads >= 4:
                                time.sleep(1)
                            t = threading.Thread(target=downloadImage, args=[
                                child.attrib["file_url"], searchString])
                            numthreads += 1
                            t.start()
                        time.sleep(0.2)
                except(IndexError):
                    print "End of results"
                    break
            print "Gelbooru: Finished searching"