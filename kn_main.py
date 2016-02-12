import json
import sqlite3
import markdown
from markdown.extensions.toc import TocExtension
import jinja2

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

	sql_stmt = '''
		SELECT
			*
		FROM kn_contents
		INNER JOIN kn_author
			ON kn_contents.author_id = kn_author.id
		WHERE kn_contents.id = ?
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [ 1]):
		dict_data=row

	sql_stmt = '''
		SELECT
			*
		FROM kn_contents_tags
		INNER JOIN kn_tags
			ON kn_contents_tags.tag_id = kn_tags.id
		WHERE content_id = ?
	'''
	for row_tag in c.execute(sql_stmt, [ 1]):
		tags.append(row_tag['tag'])

	c.close()
	dict_data["tags"] = tags
	return(json.dumps(dict_data, sort_keys=True, indent=4))

def kn_print_content(json_data):
	root = json.loads(json_data)
	con = markdown.markdown(root['context'], extensions=[TocExtension(baselevel=2)], output_format='xhtml5')
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('./tests/', encoding='utf8'))
	htmltmpl = env.get_template('contents.material.html.ja')
	ret = htmltmpl.render({'root':root, 'markdown':con})
	return ret

if __name__ == '__main__':
	json_data = kn_read_content('./tests/kn.sqlite3')
	print(kn_print_content(json_data))
