import json
import sqlite3
import markdown
from markdown.extensions.toc import TocExtension

def kn_read_content(kn_db):
	conkeylist = ["id", "published", "updated", "title", "author", "context", "status", "next_id", "prev_id"]
	conn = sqlite3.connect(kn_db)
	tags = []

	c = conn.cursor()

	for row in c.execute('SELECT kn_contents.id, published, updated, title, kn_author.name, context, status, next_id, prev_id FROM kn_contents INNER JOIN kn_author ON kn_contents.author = kn_author.id WHERE kn_contents.id = ? LIMIT 1;', [ 1]):
		dict_data=dict(zip(conkeylist,list(row)))

	for row_tag in c.execute('SELECT kn_tags.tag FROM kn_contents_tags INNER JOIN kn_tags ON kn_contents_tags.tag_id = kn_tags.id WHERE content_id = ?;', [ 1]):
		tags.append(row_tag[0])

	c.close()
	dict_data["tags"] = tags
	return json.dumps(dict_data, sort_keys=True, indent=4)

if __name__ == '__main__':
	json_data = kn_read_content('./test/kn.sqlite3')

	root = json.loads(json_data)
	print('<article itemscope itemType="http://schema.org/BlogPosting">')
	print('<h2 itemprop="headline">', root["title"], '</h2>')
	print('<footer>')
	print('<span>公開日: <time itemprop="datePublished">', root["published"] + 'Z', '</time></span>')
	print('<span>更新日: <time itemprop="dateModified">', root["updated"] + 'Z', '</time></span>')
	print('<span itemprop="author">作者: ', root["author"], '</span>')
	print('</footer>')
	print('<ul class="tags" itemprop="articleSection">')
	for tag in root["tags"]:
		print('<li>', tag, '</li>')

	print('</ul>')
	print('<div itemprop="articleBody">')
	print( markdown.markdown(root["context"], extensions=[TocExtension(baselevel=2)], output_format="xhtml5"))
	print('</div>')
	print('</article>')
