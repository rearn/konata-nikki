import json
import sqlite3
import markdown
from markdown.extensions.toc import TocExtension

conkeylist = ["id", "published", "updated", "title", "author", "context", "status", "next_id", "prev_id"]
conn = sqlite3.connect('kn.sqlite3')
tags = []

c = conn.cursor()

for row in c.execute('SELECT kn_contents.id, published, updated, title, kn_author.name, context, status, next_id, prev_id FROM kn_contents INNER JOIN kn_author ON kn_contents.author = kn_author.id WHERE kn_contents.id = ? LIMIT 1;', [ 1]):
	dict_data=dict(zip(conkeylist,list(row)))
	#json_data=json.dumps(dict_data,  sort_keys=True, indent=4)
	#print(json_data)

for row_tag in c.execute('SELECT kn_tags.tag FROM kn_contents_tags INNER JOIN kn_tags ON kn_contents_tags.tag_id = kn_tags.id WHERE content_id = ?;', [ 1]):
	tags.append(row_tag[0])

dict_data["tags"] = tags
json_data=json.dumps(dict_data,  sort_keys=True, indent=4)
print(json_data)


root = json.loads(json_data)
print( markdown.markdown(root["context"], extensions=[TocExtension(baselevel=3)]))
print( root["tags"] )
