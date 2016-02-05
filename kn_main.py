import json
import sqlite3
import markdown
from markdown.extensions.toc import TocExtension

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def kn_read_content(kn_db):
	conn = sqlite3.connect(kn_db)
	tags = []

	conn.row_factory= dict_factory
	c = conn.cursor()

	for row in c.execute('SELECT * FROM kn_contents INNER JOIN kn_author ON kn_contents.author_id = kn_author.id WHERE kn_contents.id = ? LIMIT 1;', [ 1]):
		dict_data=row

	for row_tag in c.execute('SELECT * FROM kn_contents_tags INNER JOIN kn_tags ON kn_contents_tags.tag_id = kn_tags.id WHERE content_id = ?;', [ 1]):
		tags.append(row_tag['tag'])

	c.close()
	dict_data["tags"] = tags
	return(json.dumps(dict_data, sort_keys=True, indent=4))

def kn_print_content(json_data):
	root = json.loads(json_data)
	tlist = []
	tlist.extend(['<article itemscope itemType="http://schema.org/BlogPosting">'])
	tlist.extend(['<h2 itemprop="headline">', root["title"], '</h2>'])
	tlist.extend(['<footer>'])
	tlist.extend(['<span>公開日: <time itemprop="datePublished">', root["published"] + 'Z', '</time></span>'])
	tlist.extend(['<span>更新日: <time itemprop="dateModified">', root["updated"] + 'Z', '</time></span>'])
	tlist.extend(['<span itemprop="author">作者: ', root["author"], '</span>'])
	tlist.extend(['</footer>'])
	tlist.extend(['<ul class="tags" itemprop="articleSection">'])
	for tag in root["tags"]:
		tlist.extend(['<li>', tag, '</li>'])

	tlist.extend(['</ul>'])
	tlist.extend(['<div itemprop="articleBody">'])
	tlist.extend([markdown.markdown(root["context"], extensions=[TocExtension(baselevel=2)], output_format="xhtml5")])
	tlist.extend(['</div>'])
	tlist.extend(['</article>'])
	return(''.join(tlist))

if __name__ == '__main__':
	json_data = kn_read_content('./tests/kn.sqlite3')
	print(kn_print_content(json_data))
