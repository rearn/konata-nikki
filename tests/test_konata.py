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
                'nav': {},
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
        assumed = [
            {
                'id': 1,
                'title': 'konata nikki test'
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
            'title': 'テストじゃないか',
            'context': '# リストのテスト\n' + \
                '- 本稼働でこんなの見せられないよ\n' + \
                '    - ですよねー\n' + \
                '\n' + \
                'いやー、テストってほんといいものですね。\n'
        }

        json_data = json.dumps([dict], sort_keys=True, indent=4)
        r = konata.write_content('./tests/kn.sqlite3', json_data)
        konata.update_status('./tests/kn.sqlite3', r[0]['id'], '200')

        ret = json.loads(konata.read_content(self.db, r[0]['id']))
        assumed = {
            'prev': {
                'id': 1,
                'title': 'konata nikki test'
            }
        }
        self.assertEqual(ret[0]['updated'], dict['updated'])
        self.assertEqual(ret[0]['published'], '2016-06-18 18:47:05')
        self.assertEqual(ret[0]['title'], dict['title'])
        self.assertEqual(ret[0]['context'], dict['context'])
        self.assertEqual(ret[0]['nav'], assumed)

    def test_now_time(self):
        self.assertEqual(konata.now_time(), '2016-06-18 18:47:05')

if __name__ == '__main__':
    unittest.main()
