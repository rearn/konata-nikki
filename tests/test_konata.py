import unittest
import json
import konata

class test_konata(unittest.TestCase):

	def setUp(self):
		self.db = './tests/kn.sqlite3'
		konata.test = True

	def test_read_site(self):
		ret = json.loads(konata.read_site(self.db))
		assumed = {
			'id': 1,
			'begun': '2015-09-09 10:15:44',
			'updated': '2015-09-09 10:15:44',
			'title': 'kn_test_site',
			'abstract': 'テストページだす'
		}
		self.assertEqual(ret, assumed)

	def test_read_content(self):
		ret = json.loads(konata.read_content(self.db, 1))
		assumed = [
			{
				'nav': {},
				'title': 'jubeat_saucer_jubegraph_bot',
				'published': '2015-09-09 10:15:44',
				'id': 1,
				'context': '\nはじめに\n===========================\nこのソフトは、[jubegraph](http://jubegraph.dyndns.org/jubeat_saucer/)に自動でアップデートするために開発したソフトです。\nそのため、いろいろとお粗末なところがあります。\nまた、このソフトは[KONAMI](http://p.eagate.573.jp/)及び[jubegraph](http://jubegraph.dyndns.org/jubeat_saucer/)とは、一切関係ありません。\n\n仕様環境\n===========================\nこのソフトは、以下のソフトを必要とします。\n\n* OpenSSL\n* BSDソケット\n\nそのため、Unix環境が必要と思われます。\n\nライセンス\n===========================\nライセンスは三条項BSDライセンスです。\n詳しくは、LICENSEファイルをご覧ください。',
				'updated': '2015-09-09 10:15:44',
				'author': 'name',
				'status': '200',
				'tags': [
					{
						'tag': 'test',
						'id': 1
					},
					{
						'tag': 'tast2',
						'id': 2
					}
				]
			}
		]
		self.assertEqual(ret, assumed)

	def test_read_tag(self):
		ret = json.loads(konata.read_tag(self.db, 1))
		assumed = {
			'tag_name': 'test',
			'tags': [
				{
					'id': 1,
					'title': 'jubeat_saucer_jubegraph_bot'
				}
			]
		}
		self.assertEqual(ret, assumed)

		ret = json.loads(konata.read_tag(self.db, 2))
		assumed = {
			'tags': [
				{
					'id': 1,
					'title': 'jubeat_saucer_jubegraph_bot'
				}
			],
			'tag_name': 'tast2'
		}
		self.assertEqual(ret, assumed)

	def test_contents_list(self):
		ret = json.loads(konata.contents_list(self.db))
		assumed = [
			{
				'id': 1,
				'title': 'jubeat_saucer_jubegraph_bot'
			}
		]
		self.assertEqual(ret, assumed)

	def test_tags_list(self):
		ret = json.loads(konata.tags_list(self.db))
		assumed = [
			{
				'id': 1,
				'tag': 'test',
				'count': 1
			},
			{
				'id': 2,
				'tag': 'tast2',
				'count': 1
			}
		]
		self.assertEqual(ret, assumed)

	def test_write_content(self):
		dict = {
			'updated': '2016-02-26 08:15:44',
			'title': 'テストだにぃ',
			'context': '\n# 基本方針\nこんなこと書いとかないと、絶対に横にそれるので\n\n- 過去の環境を切り捨てる\n	- 例えば、python2とかhtml4とか\n- 出来る限り構造とデザインを分ける\n- コミットのコメントは一行目は英語で\n	- 2行目以降と、メモ、ソース内のコメントは日本語可\n- こだわりすぎない\n- `(=ω=.)` <- このAAは関係ない\n	- 関係ないったら関係ない！！！\n'
		}

		json_data = json.dumps([dict], sort_keys=True, indent=4)
		r = konata.write_content('./tests/kn.sqlite3', json_data)
		konata.update_status('./tests/kn.sqlite3', r[0]['id'], '200')

		ret = json.loads(konata.read_content(self.db, r[0]['id']))
		assumed = {
			'prev': {
				'id': 1,
				'title': 'jubeat_saucer_jubegraph_bot'
			}
		}
		self.assertEqual(ret[0]['updated'], dict['updated'])
		self.assertEqual(ret[0]['published'], '2016/06/18 18:47:05')
		self.assertEqual(ret[0]['title'], dict['title'])
		self.assertEqual(ret[0]['context'], dict['context'])
		self.assertEqual(ret[0]['nav'], assumed)

if __name__ == '__main__':
	unittest.main()
