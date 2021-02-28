#!/usr/bin/env python3
import requests
import re
import util.request_helper
import util.request_helper
from fake_headers import Headers

def sitemap_reader(sitemap_indicator,element,sitemap_url,file_store_location):
    try:
        requests_data = {}        
        random_header = Headers(browser='firefox',os='win',headers=True,)
        headers = util.request_helper.replace_browser_versions(random_header.generate())
        requests_data['headers'] = headers
        requests_data['url'] = sitemap_url
        sitemap_str = requests.get(**requests_data)

        for item in re.finditer(r"<"+str(element)+">(.*?)<\/"+str(element)+">", sitemap_str.text, re.MULTILINE):
            if sitemap_indicator in item.group(1):
                print ('Going deeper to ',item.group(1))
                sitemap_reader(sitemap_indicator,element,item.group(1),file_store_location)
            else:
                with open(file_store_location,'a') as sitemap_file:
                    sitemap_file.write(item.group(1) + '\n')

    except Exception as e:
        print(e)
