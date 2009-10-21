""" run the script from the dir which has the worpdress export file
    
    give the base path of the HiSlain blog as a command-line argument.
    remember the base path, not directly the out folder  """
import sys
import os
import elementtree.ElementTree as ET
import codecs
from datetime import datetime
def parse_xml():
    tree = ET.parse("wp.xml")
    list_of_blog_entries = []
    results = {}

    for item in tree.findall("channel/item"):
        results['title'] = item.find("title").text
        permalink = ()
        permalink = item.find("link").text.rpartition("/")
        results['link'] = permalink[2]
        results['pubdate'] = str(datetime.strptime(item.find("pubDate").text,\
                             "%a, %d %b %Y %H:%M:%S +0000"))
        results['body'] = item.find( \
                      "{http://purl.org/rss/1.0/modules/content/}encoded").text
        results['post_type'] = item.find(\
                          "{http://wordpress.org/export/1.0/}post_type").text
        results['tags'] = [] 
        tags = item.findall("category")
        for c in tags:
            if c.get('domain')=='tag':
                if c.get('nicename') != None:
                    results['tags'].append(c.get('nicename'))
        list_of_blog_entries.append(results)
        results = {}
    return list_of_blog_entries


def write_files(blog_path,blog_entries):
    if not os.path.exists(blog_path):
        print "Invalid path"
    else:
        for item in blog_entries:
            if item['post_type'] == 'post':
                file_name = item['link'].split('.')[0]
                post_file = blog_path+"posts/"+file_name+".post"
            else:
                file_name = item['link']
                post_file = blog_path+"pages/"+file_name+".page"
            fsock = open(post_file,'w')
            fsock.write(item['title']+"\n")
            if item['post_type'] == 'post':
                fsock.write("permalink: "+item['link']+"\n")
                fsock.write("tags: ") 
                for tag in item['tags']:
                    fsock.write(tag+",")
                fsock.write("\n")
                fsock.write("published: ")
                fsock.write(item['pubdate'])
            fsock.write("\n\n")
            body = item['body'].encode('utf-8')
            fsock.write(body)

if __name__=='__main__':
    blog_path = sys.argv[1]        
    blog_entries = parse_xml()
    write_files(blog_path, blog_entries)
    
