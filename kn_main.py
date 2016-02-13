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

def kn_search_uri(id, type):
	if type == 'content':
		return ''.join('/content/',id)
	if type == 'tag':
		return ''.join('/tag/',id)

def kn_read_content(kn_db):
	conn = sqlite3.connect(kn_db)
	tags = []
	dict_data = {}
	nav = {}

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			kn_sites.id,
			begun,
			updated,
			title,
			abstract,
			latest_content_id
		FROM kn_sites
		INNER JOIN kn_author
			ON kn_sites.main_author_id = kn_author.id
		WHERE kn_sites.id = ?
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [ 1]): # site 1
		dict_data['site']=row

	sql_stmt = '''
		SELECT
			kn_contents.id,
			published,
			updated,
			title,
			kn_author.author,
			context,
			status,
			next_id,
			prev_id
		FROM kn_contents
		INNER JOIN kn_author
			ON kn_contents.author_id = kn_author.id
		WHERE kn_contents.id = ?
		LIMIT 1
	'''
	dict_data['contents'] = list(c.execute(sql_stmt, [ 1]))

	sql_stmt = '''
		SELECT
			kn_tags.tag
		FROM kn_contents_tags
		INNER JOIN kn_tags
			ON kn_contents_tags.tag_id = kn_tags.id
		WHERE content_id = ?
	'''
	for row_tag in c.execute(sql_stmt, [ 1]):
		tags.append(row_tag['tag'])

	sql_stmt = '''
		SELECT
			id,
			title
		FROM kn_sites
		WHERE content_id = ?
	'''
	if dict_data['contents'][0]['prev_id'] is not None:
		prev = c.execute(sql_stmt, dict_data['contents'][0]['prev_id'])
		prev[0]['uri'] = kn_search_uri(prev[0]['id'], 'content')
		nav['prev'] = prev[0]
	del dict_data['contents'][0]['prev_id']
	if dict_data['contents'][0]['next_id'] is not None:
		next = c.execute(sql_stmt, dict_data['contents'][0]['next_id'])
		next[0]['uri'] = kn_search_uri(next[0]['id'], 'content')
		nav['next'] = next[0]
	del dict_data['contents'][0]['next_id']
	dict_data['contents'][0]['nav'] = nav

	c.close()
	dict_data['contents'][0]['tags'] = tags
	return(json.dumps(dict_data, sort_keys=True, indent=4))

def kn_print_content(json_data):
	root = json.loads(json_data)
	con = markdown.markdown(root['contents'][0]['context'], extensions=[TocExtension(baselevel=2)], output_format='xhtml5')
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('./tests/', encoding='utf8'))
	htmltmpl = env.get_template('contents.material.html.ja')
	ret = htmltmpl.render({'root':root['contents'][0], 'markdown':con})
	return ret

if __name__ == '__main__':
	json_data = kn_read_content('./tests/kn.sqlite3')
	print(json_data) # debug
	print(kn_print_content(json_data))
