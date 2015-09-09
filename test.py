import json
import sqlite3
import markdown
from markdown.extensions.toc import TocExtension

conkeylist = ["id", "published", "updated", "title", "author", "context", "status", "next_id", "prev_id"]
conn = sqlite3.connect('kn.sqlite3')

c = conn.cursor()

for row in c.execute('SELECT id, published, updated, title, author, context, status, next_id, prev_id FROM kn_contents WHERE id = ?;', [ 1]):
	json_data=json.dumps(dict(zip(conkeylist,list(row))),  sort_keys=True, indent=4)
	#print(json_data)
	
	root = json.loads(json_data)
	print( markdown.markdown(root["context"], extensions=[TocExtension(baselevel=2)]))