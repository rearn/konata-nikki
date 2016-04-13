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

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

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
		  AND status LIKE '2__'
		LIMIT 1
	'''
	dict_data['contents'] = list(c.execute(sql_stmt, [contents_id]))
	if len(dict_data['contents']) == 0:
		raise ValueError('404 Not Found')
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
	dict_data['contents'][0]['nav'] = nav

	c.close()
	conn.close()
	dict_data['contents'][0]['tags'] = tags
	return(json.dumps(dict_data, sort_keys=True, indent=4))

def kn_read_tag(kn_db, tags_id):
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
			title,
			status
		FROM kn_contents_tags
		INNER JOIN kn_contents
			ON kn_contents_tags.content_id = kn_contents.id
		WHERE tag_id = ?
		  AND status LIKE '2__'
	'''
	dict_data['tags'] = list(c.execute(sql_stmt, [tags_id]))
	sql_stmt = '''
		SELECT tag
		FROM kn_tags
		WHERE id = ?
	'''
	for row_tag in c.execute(sql_stmt, [tags_id]):
		dict_data['tag_name'] = row_tag['tag']
	c.close()
	conn.close()
	return(json.dumps(dict_data, sort_keys=True, indent=4))


def kn_update_status(kn_db, id, status):
	dict_data = {}
	conn = sqlite3.connect(kn_db)

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT status
		FROM kn_contents
		WHERE id = ?
		LIMIT 1
	'''

	for row in c.execute(sql_stmt, [id]):
		now_status = row['status']

	if now_status[0:2] != status[0:2]:
		sql_stmt = '''
			UPDATE kn_contents
			SET status = ?
			WHERE id = ?
		'''
		c.execute(sql_stmt, [status, id])
		conn.commit()

	c.close()
	conn.close()
	return


def kn_write_content(kn_db, write_json):
	conn = sqlite3.connect(kn_db)
	write_list=[]

	write_date = json.loads(write_json)

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT id
		FROM kn_contents
		ORDER BY id DESC
		LIMIT 1
	'''
	for row in c.execute(sql_stmt):
		last = row['id']
		break
	else:
		last = 0

	sql_stmt = '''
		INSERT INTO
			kn_contents (
				site_id,
				published,
				title,
				author_id,
				natural_lang,
				markup_lang,
				context
			)
		VALUES (?,?,?,?,?,?,?)
	'''

	for d in write_date:
		t = [1, d['published'], d['title'], 1, 'ja-JP', 'markdown', d['context']]
		write_list.append(tuple(t))
	print(write_list)
	c.executemany(sql_stmt, write_list)
	conn.commit()

	sql_stmt = '''
		SELECT
			id,
			site_id
		FROM kn_contents
		WHERE id > ?
	'''
	l = c.execute(sql_stmt, [last])
	conn.commit()
	c.close()
	conn.close()
	return list(l)

if __name__ == '__main__':
	dict = {
		'published': '2016-02-26 08:15:44',
		'title': 'テストだにぃ',
		'context': '''
# 基本方針
こんなこと書いとかないと、絶対に横にそれるので

- 過去の環境を切り捨てる
	- 例えば、python2とかhtml4とか
- 出来る限り構造とデザインを分ける
- コミットのコメントは一行目は英語で
	- 2行目以降と、メモ、ソース内のコメントは日本語可
- こだわりすぎない
- `(=ω=.)` <- このAAは関係ない
	- 関係ないったら関係ない！！！

	'''
	}
	t = []
	t.append(dict)
	json_data = json.dumps(t, sort_keys=True, indent=4)
	print(json_data) # debug
	r = kn_write_content('./tests/kn.sqlite3', json_data)
	#r = [{'id': 2, 'site_id': 1}]
	kn_update_status('./tests/kn.sqlite3', r[0]['id'], '200')

