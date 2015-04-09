#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
This script converts OSM file into JSON format
For more details on conversion see comments in P2-6/data.py

Input file: 	saint-petersburg_russia.osm
Output:		saint-petersburg_russia.osm.json
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    node['created'] = {}
    if element.tag == "node" or element.tag == "way" :
        for a in element.attrib:
            if a in CREATED:
                node['created'][a] = element.attrib[a]
            elif a != 'lat' and a != 'lon':
                node[a] = element.attrib[a]
        
        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]

        # process 2nd level tags    
        for child in element:
            if 'k' in child.attrib:
                key = child.attrib['k']
                val = child.attrib['v']
                if problemchars.search(key) or key.count(':') > 1:
                    continue
                if key.startswith('addr:'):
                    if 'address' not in node:
                        node['address'] = {}
                    node['address'][key.replace('addr:', '')]= val
            if child.tag == 'nd':
                 if 'node_refs' not in node:
                     node['node_refs'] = []
                 node['node_refs'].append(child.attrib['ref'])
        node['type'] = element.tag
        #pprint.pprint(node)
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def main():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.

    #data = process_map('saint-petersburg_russia.osm', False)
    data = process_map('1', False)
    #pprint.pprint(data)
    

if __name__ == "__main__":
    main()