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
from datetime import datetime

test = False

def now_time():
	if test:
		return '2016/06/18 18:47:05'
	else:
		return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def read_site(db):
	conn = sqlite3.connect(db)

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			id,
			begun,
			updated,
			title,
			abstract
		FROM kn_sites
		WHERE id = ?
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [1]):
		dict_data = row

	c.close()
	conn.close()
	return(json.dumps(dict_data, sort_keys=True, indent=4))

def read_content(db, contents_id):
	conn = sqlite3.connect(db)
	tags = []
	dict_data = {}
	nav = {}

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			kn_contents.id,
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
	contents = list(c.execute(sql_stmt, [contents_id]))
	if len(contents) == 0:
		return(json.dumps(contents, sort_keys=True, indent=4))

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
		ORDER BY id ASC
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [contents_id]):
		nav['next'] = row
	sql_stmt = '''
		SELECT
			id,
			title
		FROM kn_contents
		WHERE id < ?
		  AND status LIKE '2__'
		ORDER BY id DESC
		LIMIT 1
	'''
	for row in c.execute(sql_stmt, [contents_id]):
		nav['prev'] = row
	contents[0]['nav'] = nav

	c.close()
	conn.close()
	contents[0]['tags'] = tags
	return(json.dumps(contents, sort_keys=True, indent=4))

def read_tag(db, tags_id):
	conn = sqlite3.connect(db)
	tags = []
	dict_data = {}
	nav = {}

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			kn_contents.id,
			title
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

def contents_list(db):
	conn = sqlite3.connect(db)

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			id,
			title
		FROM kn_contents
		WHERE status LIKE '2__'
		ORDER BY id DESC
	'''

	contents = list(c.execute(sql_stmt))
	c.close()
	conn.close()
	return(json.dumps(contents, sort_keys=True, indent=4))

def tags_list(db):
	conn = sqlite3.connect(db)
	tags = []

	conn.row_factory= dict_factory
	c = conn.cursor()

	sql_stmt = '''
		SELECT
			kn_tags.id,
			tag,
			count(kn_tags.id)
		FROM kn_contents_tags
		LEFT JOIN kn_tags
			ON kn_contents_tags.tag_id = kn_tags.id
		GROUP BY tag
		ORDER BY
			count(kn_tags.id) DESC,
			kn_tags.id ASC
	'''

	for row in c.execute(sql_stmt):
		row['count'] = row['count(kn_tags.id)']
		del(row['count(kn_tags.id)'])
		tags.append(row)

	c.close()
	conn.close()
	return(json.dumps(tags, sort_keys=True, indent=4))

def update_status(db, id, status):
	dict_data = {}
	conn = sqlite3.connect(db)

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


def write_content(db, write_json):
	conn = sqlite3.connect(db)
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
				updated,
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
		t = [
			d['updated'],
			now_time(),
			d['title'],
			1,
			'ja-JP',
			'markdown',
			d['context']
		]
		write_list.append(tuple(t))
	c.executemany(sql_stmt, write_list)
	conn.commit()

	sql_stmt = '''
		SELECT id
		FROM kn_contents
		WHERE id > ?
	'''
	l = c.execute(sql_stmt, [last])
	ret = list(l)
	c.close()
	conn.close()
	return ret

if __name__ == '__main__':
	dict = {
		'updated': '2016-02-26 08:15:44',
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
	r = write_content('./tests/kn.sqlite3', json_data)
	#r = [{'id': 2, 'site_id': 1}]
	update_status('./tests/kn.sqlite3', r[0]['id'], '200')

