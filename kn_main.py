#!/usr/bin/env python3
#
# Copyright (C) 2016  minamibashi rearn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
		return ''.join(['/content/', str(id)])
	if type == 'tag':
		return ''.join(['/tag/', str(id)])

def kn_read_content(kn_db, contents_id):
	conn = sqlite3.connect(kn_db)
	tags = []
	dict_data = {}
	nav = {}

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			kn_contents.id,
			site_id,
			published,
			updated,
			title,
			kn_author.author,
			context,
			status
		FROM kn_contents
		INNER JOIN kn_author
			ON kn_contents.author_id = kn_author.id
		WHERE kn_contents.id = ?
		LIMIT 1
	'''
	dict_data['contents'] = list(c.execute(sql_stmt, [contents_id]))
	print(dict_data)
	sql_stmt = '''
		SELECT
			kn_sites.id,
			top_uri,
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
	for row in c.execute(sql_stmt, [dict_data['contents'][0]['site_id']]):
		dict_data['site'] = row

	sql_stmt = '''
		SELECT
			kn_tags.id,
			kn_tags.tag
		FROM kn_contents_tags
		INNER JOIN kn_tags
			ON kn_contents_tags.tag_id = kn_tags.id
		WHERE content_id = ?
	'''
	for row_tag in c.execute(sql_stmt, [contents_id]):
		row_tag['uri'] = kn_search_uri(row_tag['id'], 'tag')
		tags.append(row_tag)

	sql_stmt = '''
		SELECT
			id,
			title
		FROM kn_contents
		WHERE id > ?
		  AND status LIKE '2__'
		  AND site_id = ?
		ORDER BY id ASC
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [contents_id, dict_data['site']['id']]):
		nav['next'] = row
		nav['next']['uri'] = kn_search_uri(row['id'], 'content')
	sql_stmt = '''
		SELECT
			id,
			title
		FROM kn_contents
		WHERE id < ?
		  AND status LIKE '2__'
		  AND site_id = ?
		ORDER BY id DESC
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [contents_id, dict_data['site']['id']]):
		nav['prev'] = row
		nav['prev']['uri'] = kn_search_uri(row['id'], 'content')
	dict_data['contents'][0]['nav'] = nav

	c.close()
	dict_data['contents'][0]['tags'] = tags
	return(json.dumps(dict_data, sort_keys=True, indent=4))

def kn_temp_proc(env, temp_file, temp_dict):
	htmltmpl = env.get_template(temp_file)
	return htmltmpl.render(temp_dict)


def kn_print_content(json_data):
	root = json.loads(json_data)
	con = markdown.markdown(root['contents'][0]['context'], extensions=[TocExtension(baselevel=3)], output_format='xhtml5')
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('./material/', encoding='utf8'))

	test = {'next': {'uri': 'aaa', 'title': 'ee'}}
	return kn_temp_proc(env, 'contents.html.ja', {'nav':root['contents'][0]['nav'], 'contents': root['contents'], 'site': root['site'], 'markdown': con})
	#return kn_temp_proc(env, 'contents.html.ja', {'nav': test, 'contents': root['contents'], 'site': root['site'], 'markdown': con})

if __name__ == '__main__':
	json_data = kn_read_content('./tests/kn.sqlite3', 1)
	print(json_data) # debug
	print(kn_print_content(json_data))
