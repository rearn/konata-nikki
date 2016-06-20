import unittest
import main

class test_main(unittest.TestCase):
    def test_make_content(self):
        ret = main.make_content('# テスト\ntestなのですよー\n\n')
        self.assertEqual(ret, '<h1>テスト</h1>\n<p>testなのですよー</p>')


class test_main_flask(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        main.konata.test = True

    def tearDown(self):
        pass

    def test_content_list(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertRegex(rv.data.decode(), '<title>kn_test_site</title>')
        self.assertRegex(rv.data.decode(),
            '<a href="/content/1">jubeat_saucer_jubegraph_bot</a>')

    def test_tag_list(self):
        rv = self.app.get('/tag/')
        self.assertEqual(rv.status_code, 200)
        self.assertRegex(rv.data.decode(), '<a href="/tag/1">test')
        self.assertRegex(rv.data.decode(), '<a href="/tag/2">tast2')

    def test_content_success(self):
        rv = self.app.get('/content/1')
        self.assertEqual(rv.status_code, 200)
        self.assertRegex(rv.data.decode(), '<p><a href="/">目次に戻る</a></p>')

    def test_content_error(self):
        rv = self.app.get('/content/42')
        self.assertEqual(rv.status_code, 404)
        self.assertRegex(rv.data.decode(),
            '見つかりません。アドレスが間違っていると思われます。')

    def test_tag_success(self):
        rv = self.app.get('/tag/1')
        self.assertEqual(rv.status_code, 200)
        self.assertRegex(rv.data.decode(),
            '<li><a href="/content/1">jubeat_saucer_jubegraph_bot</a></li>')

    def test_tag_error(self):
        rv = self.app.get('/tag/42')
        self.assertEqual(rv.status_code, 404)
        self.assertRegex(rv.data.decode(),
            '見つかりません。アドレスが間違っていると思われます。')

    def test_write_step1_get(self):
        rv = self.app.get('/write/step1')
        self.assertEqual(rv.status_code, 302)

    def test_write_step2_get(self):
        rv = self.app.get('/write/step2')
        self.assertEqual(rv.status_code, 302)

    def test_write_get(self):
        rv = self.app.get('/write/')
        self.assertEqual(rv.status_code, 200)
        self.assertRegex(rv.data.decode(),
            '<form method="post" action="/write/step1">')
        self.assertRegex(rv.data.decode(),
            '<input type="submit" value="送信する">')
        self.assertRegex(rv.data.decode(),
            '<input type="text" name="title" size="80">')
        self.assertRegex(rv.data.decode(),
            '<textarea name="context" cols="80" rows="24"></textarea>')

    def test_write_post(self):
        rv = self.app.post('/write/step1', data=dict(
            title='にぱ〜',
            context='テストなのですよ〜'
        ))
        self.assertRegex(rv.data.decode(),
            '<p>以下の様に表示されます。問題ありませんか？</p>')
        self.assertRegex(rv.data.decode(), '2016-06-18 18:47:05')
        self.assertRegex(rv.data.decode(), '<h2 itemprop="headline">にぱ〜</h2>')
        self.assertRegex(rv.data.decode(), '<p>テストなのですよ〜</p>')

        rv = self.app.post('/write/', data=dict(
            date='2016-06-18 18:47:05'
        ))
        self.assertEqual(rv.status_code, 200)
        self.assertRegex(rv.data.decode(),
            '<form method="post" action="/write/step1">')
        self.assertRegex(rv.data.decode(),
            '<input type="submit" value="送信する">')
        self.assertRegex(rv.data.decode(),
            '<input type="text" name="title" size="80" value="にぱ〜">')
        self.assertRegex(rv.data.decode(),
            '<textarea name="context" cols="80" rows="24">テストなのですよ〜</textarea>')

    def test_write_step2_post(self):
        rv = self.app.post('/write/step1', data=dict(
            title='にぱ〜',
            context='テストなのですよ〜'
        ))
        self.assertRegex(rv.data.decode(),
            '<p>以下の様に表示されます。問題ありませんか？</p>')
        self.assertRegex(rv.data.decode(), '2016-06-18 18:47:05')
        self.assertRegex(rv.data.decode(), '<h2 itemprop="headline">にぱ〜</h2>')
        self.assertRegex(rv.data.decode(), '<p>テストなのですよ〜</p>')

        rv = self.app.post('/write/step2', data=dict(
            date='2016-06-18 18:47:05'
        ), follow_redirects=True)
        self.assertRegex(rv.data.decode(),
            '<title>にぱ〜 - kn_test_site</title>')
        self.assertRegex(rv.data.decode(), '<h2 itemprop="headline">にぱ〜</h2>')
        self.assertRegex(rv.data.decode(),
            '<time itemprop="datePublished">2016-06-18 18:47:05</time>')
        self.assertRegex(rv.data.decode(), '<p>テストなのですよ〜</p>')


if __name__ == '__main__':
    unittest.main()
