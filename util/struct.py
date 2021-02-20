#!/usr/bin/env python3
import requests
import re

def sitemap_reader(sitemap_indicator,element,kwargs,stored_items = []):
    try:
        sitemap_str = requests.get(**kwargs)

        for item in re.finditer(r"<"+str(element)+">(.*?)<\/"+str(element)+">", sitemap_str.text, re.MULTILINE):
            if sitemap_indicator in item.group(1):
                print ('Going deeper to ',item.group(1))
                kwargs['url'] = item.group(1)
                sitemap_reader(sitemap_indicator,element,kwargs,stored_items)
            else:
                stored_items.append(item.group(1))
    except Exception as e:
        print(e)
        return stored_items

    return stored_items
