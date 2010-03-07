""" Run the script from the directory which has the worpdress export file
    
    give the base path of the HiSlain blog as a command-line argument.
    Remember the *base path*, *not* directly the *out* folder  """
import sys
import os
import xml.etree.ElementTree as ET
import codecs
from datetime import datetime

def parse_xml():
    """ Method that parses the wordpress export file
        
        It uses elementree module to extract the needed data from wp export file
        """
    tree = ET.parse("wp.xml")
    list_of_blog_entries = []
    results = {}

    for item in tree.findall("channel/item"):
        results['title'] = item.find("title").text
        permalink = ()
        permalink = item.find("link").text.rpartition("/")
        results['link'] = permalink[2]
        results['pubdate'] = parser.parse(item.find("pubDate").text)
                             
        results['body'] = item.find( \
                      "{http://purl.org/rss/1.0/modules/content/}encoded").text
        results['post_type'] = item.find(\
                          "{http://wordpress.org/export/1.0/}post_type").text
        results['tags'] = [] 
        tags = item.findall("category")
        for entry in tags:
            if entry.get('domain')=='tag':
                if entry.get('nicename') != None:
                    results['tags'].append(entry.get('nicename'))
        list_of_blog_entries.append(results)
        results = {}
    return list_of_blog_entries


def write_files(blog_path, blog_entries):
    """ Writes the posts, pages entries readable by HiSlain"""
    if not os.path.exists(blog_path):
        print "Invalid path"
    else:
        for item in blog_entries:
            if item['post_type'] == 'post':
                file_name = item['link'].split('.')[0]
                post_file = os.path.join(blog_path, "posts", file_name+'.post')
            else:
                file_name = item['link']
                post_file = os.path.join(blog_path, "pages", file_name+".page")
            fsock = open(post_file,'w')
            fsock.write(item['title']+"\n")
            if item['post_type'] == 'post':
                fsock.write("permalink: "+item['link']+"\n")
                fsock.write("tags: ") 
                for tag in item['tags']:
                    fsock.write(tag+",")
                fsock.write("\n")
                fsock.write("published: ")
                fsock.write(str(item['pubdate']))
            fsock.write("\n\n")
            body = item['body']
            fsock.write(body)
            fsock.close()        

if __name__ == '__main__':
    BlogPath = sys.argv[1]        
    BlogEntries = parse_xml()
    write_files(BlogPath, BlogEntries)
    
