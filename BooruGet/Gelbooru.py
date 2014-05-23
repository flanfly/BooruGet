"""
Frank Hrach
Gelbooru.py
Sun Mar  9 22:29:53 EDT 2014
"""

import arguments
import Booru
import Filter
import httplib2
import math
import time
import xml.etree.ElementTree as ET


class GelbooruDownloader(Booru):
    """
    Holds all the methods and data required to download files from gelbooru
    """

    url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index"
    number_per_page = 100

    searchString = ""
    target_width = -1
    target_height = -1

    page_num = 0
    number_of_pages = 1000
    number_per_page = 100

    def __init__(self, args, download_manager):
        self.search_string = args.search_string
        self.target_width = args.target_width
        self.target_height = args.target_height
        self.error = args.error
        self.verbose = args.verbose
        self.tags = args.search_string
        self.download_manager = download_manager
        self.image_filter = Filter.Filter(args)

    def get_results(self):
        """
        Connects to the server and gets a page worth of results
        """
        if self.verbose:
            print "Gelbooru: Reqesting page"
        try:
            connection = httplib2.Http(".cache")
            res, content = connection.request(
                self.url + "&tags=" + self.searchString + "&pid=" +
                str(self.page_num) + "&limit=" + str(self.number_of_pages))
            if self.verbose:
                print "\tResults recieved"
            if not res.status == 200:
                if self.verbose:
                    print "\tResponse was not 200 (" + res.status + ")"
                else:
                    print "Error with search, trying again"
                time.sleep(5000)
                self.get_results()
            if len(content) >= 0:
                if self.verbose:
                    print "\tResponse was 200"
                    print "Done"
                return ET.fromstring(content)
            else:
                return None
        except httplib2.ServerNotFoundError:
            print "Could not contact server at gelbooru.com"
            print "Retrying in 30 seconds"
            time.sleep(30)
            self.get_results()
        return None

    def download(self):
        """
        """
        #TODO write documentation for download
        # connect once to get the number of pages for the search
        root = self.get_results()
        self.number_of_pages = int(
            math.ceil(int(root.attrib["count"]) / float(len(root))))

        # sleep to ensure we are not spamming the server
        time.sleep(0.2)

        for i in range(0, self.number_of_pages + 1):

            # if call to exit is found, break out of this loop now
            #if exitapp:
                #break

            # Get page from the server
            root = self.get_results()

            if self.verbose:
                print "Gelbooru: current page: " + str(i) + " (" + \
                    str(i * self.number_per_page) + ") out of " + \
                    str(self.number_of_pages) + \
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

                    if self.image_filter.filter_result(image):
                        self.download_manager.enqueue_file(image, self.tags)
            except(IndexError):
                print "End of results"
                break
        print "Gelbooru: Finished searching"
