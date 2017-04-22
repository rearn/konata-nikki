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
            'abstract': 'テストサイトだす'
        }
        self.assertEqual(ret, assumed)

    def test_read_content(self):
        ret = json.loads(konata.read_content(self.db, 1))
        assumed = [
            {
                'id': 1,
                'title': 'konata nikki test',
                'published': '2015-09-09 10:15:44',
                'context': '最初のテストページだよ',
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
        del ret[0]['nav']
        self.assertEqual(ret, assumed)

    def test_read_tag(self):
        ret = json.loads(konata.read_tag(self.db, 1))
        assumed = {
            'tag_name': 'test',
            'tags': [
                {
                    'id': 1,
                    'title': 'konata nikki test'
                }
            ]
        }
        self.assertEqual(ret, assumed)

        ret = json.loads(konata.read_tag(self.db, 2))
        assumed = {
            'tags': [
                {
                    'id': 1,
                    'title': 'konata nikki test'
                }
            ],
            'tag_name': 'tast2'
        }
        self.assertEqual(ret, assumed)

    def test_contents_list(self):
        ret = json.loads(konata.contents_list(self.db))
        assumed = {
            'id': 1,
            'title': 'konata nikki test'
        }
        self.assertIn(assumed, ret)

    def test_tags_list(self):
        ret = json.loads(konata.tags_list(self.db))
        assumed1 = {
            'id': 1,
            'tag': 'test',
            'count': 1
        }
        assumed2 = {
            'id': 2,
            'tag': 'tast2',
            'count': 1
        }
        self.assertIn(assumed1, ret)
        self.assertIn(assumed2, ret)

    def test_write_content(self):
        dict = {
            'updated': '2016-02-26 08:15:44',
            'title': 'テストじゃないか',
            'context': '# リストのテスト\n' + \
                '- 本稼働でこんなの見せられないよ\n' + \
                '    - ですよねー\n' + \
                '\n' + \
                'いやー、テストってほんといいものですね。\n'
        }

        json_data = json.dumps([dict])
        r = json.loads(konata.write_content(self.db, json_data))
        konata.update_status(self.db, r[0]['id'], '200')

        ret = json.loads(konata.read_content(self.db, r[0]['id']))
        self.assertEqual(ret[0]['updated'], dict['updated'])
        self.assertEqual(ret[0]['published'], '2016-06-18 18:47:05')
        self.assertEqual(ret[0]['title'], dict['title'])
        self.assertEqual(ret[0]['context'], dict['context'])

    def test_now_time(self):
        self.assertEqual(konata.now_time(), '2016-06-18 18:47:05')

    def test_add_tag(self):
        json_data = json.dumps(['ラーメン'])
        r = json.loads(konata.add_tag(self.db, json_data))
        ret = json.loads(konata.read_tag(self.db, r[0]))
        self.assertEqual(ret['tag_name'], 'ラーメン')

    def test_add_tag_list(self):
        json_data = json.dumps(['うどん', 'そば'])
        r = json.loads(konata.add_tag(self.db, json_data))
        ret = json.loads(konata.read_tag(self.db, r[0]))
        self.assertEqual(ret['tag_name'], 'うどん')
        ret = json.loads(konata.read_tag(self.db, r[1]))
        self.assertEqual(ret['tag_name'], 'そば')

    def test_add_content_to_tag(self):
        json_data = json.dumps(['そーめん'])
        r1 = json.loads(konata.add_tag(self.db, json_data))
        dict = {
            'updated': '2016-06-20 20:51:33',
            'title': 'タグ追加テスト',
            'context': 'タグ追加できるかな？'
        }

        json_data = json.dumps([dict])
        r2 = json.loads(konata.write_content(self.db, json_data))
        konata.update_status(self.db, r2[0]['id'], '200')
        json_data = json.dumps([{
            'content': r2[0]['id'],
            'tags': r1[0]
        }])
        konata.add_content_to_tag(self.db, json_data)

        ret = json.loads(konata.read_content(self.db, r2[0]['id']))
        self.assertEqual(ret[0]['tags'][0]['tag'], 'そーめん')

    def test_rand_str64(self):
        self.assertEqual(konata.rand_str64(),
                         '0123456789' + \
                         'abcdefghijklmnopqrstuvwxyz' + \
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '42')

if __name__ == '__main__':
    unittest.main()
