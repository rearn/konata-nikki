import json
import sqlite3

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


def kn_update_status(kn_db, id, site_id, status):
	dict_data = {}
	conn = sqlite3.connect(kn_db)

	conn.row_factory= dict_factory
	c = conn.cursor()

	if status[0] == '2':
		sql_stmt = '''
			SELECT
				id,
				prev_id
			FROM kn_contents
			WHERE id > ?
			  AND status LIKE '2__'
			  AND site_id = ?
			ORDER BY id ASC
			LIMIT 1
		'''

		for row in c.execute(sql_stmt, [id, site_id,]):
			dict_data['next'] = row
			break
		else:
			temp = {'id': None, 'prev_id': None}
			dict_data['next'] = temp

		sql_stmt = '''
			SELECT
				id,
				next_id
			FROM kn_contents
			WHERE id < ?
			  AND status LIKE '2__'
			  AND site_id = ?
			ORDER BY id DESC
			LIMIT 1
		'''

		for row in c.execute(sql_stmt, [id, site_id]):
			dict_data['prev'] = row
			break
		else:
			temp = {'id': None, 'next_id': None}
			dict_data['prev'] = temp

		sql_stmt = '''
			SELECT
				id,
				prev_id,
				next_id
			FROM kn_contents
			WHERE id = ?
			  AND status LIKE '2__'
			  AND site_id = ?
			ORDER BY id DESC
			LIMIT 1
		'''

		for row in c.execute(sql_stmt, [id, site_id]):
			dict_data['now'] = row
			break
		else:
			temp = {'prev_id': None, 'next_id': None}
			dict_data['now'] = temp

		if( \
			dict_data['next']['id'] != None \
			and dict_data['prev']['id'] != None \
		) \
		and ( \
			dict_data['next']['id'] != dict_data['prev']['next_id'] \
			or dict_data['prev']['id'] != dict_data['next']['prev_id']
		):
			# error
			print('error')
			print(dict_data)

		sql_stmt = '''
			UPDATE kn_contents
			SET next_id = ?
			WHERE id = ?
		'''
		if dict_data['prev']['id']:
			c.execute(sql_stmt, [id, dict_data['prev']['id']])

		sql_stmt = '''
			UPDATE kn_contents
			SET prev_id = ?
			WHERE id = ?
		'''
		if dict_data['next']['id']:
			c.execute(sql_stmt, [id, dict_data['next']['id']])

		sql_stmt = '''
			UPDATE kn_contents
			SET
				prev_id = ?,
				next_id = ?,
				status = ?
			WHERE id = ?
		'''
		c.execute(sql_stmt, [dict_data['prev']['id'], dict_data['next']['id'], status, id])
		conn.commit()
		print('OK')
	else:
		# 未実装
		print('未実装')


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
	kn_update_status('./tests/kn.sqlite3', r[0]['id'], r[0]['site_id'], '200')
