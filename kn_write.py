import json
import sqlite3
def kn_write_content(kn_db, write_json):
	conn = sqlite3.connect(kn_db)
	write_list=[]

	write_date = json.loads(write_json)

#	conn.row_factory = dict_factory
	c = conn.cursor()

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

	return

if __name__ == '__main__':
	dict = {'published': '2016-02-26 08:15:44', 'title': 'テストだにぃ', 'context': '''
# 基本方針
こんなこと書いとかないと、絶対に横にそれるので
- 過去の環境を切り捨てる
	- 例えば、python2とかhtml4とか
- 出来る限り構造とデザインを分ける
- コミットのコメントは一行目は英語で
	 -2行目以降と、メモ、ソース内のコメントは日本語可
- こだわりすぎない
- `(=ω=.)` <- このAAは関係ない
	- 関係ないったら関係ない！！！
	'''}
	t = []
	t.append(dict)
	json_data = json.dumps(t, sort_keys=True, indent=4)
	print(json_data) # debug
	kn_write_content('./tests/kn.sqlite3', json_data)
	
