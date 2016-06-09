PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE kn_contents (
	id integer primary key autoincrement,
	published date default CURRENT_TIMESTAMP,
	updated date default CURRENT_TIMESTAMP,
	title varchar(1024) unique not null,
	author_id int,
	natural_lang char(16),
	markup_lang char(16),
	context clob,
	status char(16) default '100',
	foreign key(author_id)
		references kn_author(id)
		on update cascade
		on delete set null
);
INSERT INTO "kn_contents" VALUES(1,'2015-09-09 10:15:44','2015-09-09 10:15:44','jubeat_saucer_jubegraph_bot',1,'ja-JP','markdown','
はじめに
===========================
このソフトは、[jubegraph](http://jubegraph.dyndns.org/jubeat_saucer/)に自動でアップデートするために開発したソフトです。
そのため、いろいろとお粗末なところがあります。
また、このソフトは[KONAMI](http://p.eagate.573.jp/)及び[jubegraph](http://jubegraph.dyndns.org/jubeat_saucer/)とは、一切関係ありません。

仕様環境
===========================
このソフトは、以下のソフトを必要とします。

* OpenSSL
* BSDソケット

そのため、Unix環境が必要と思われます。

ライセンス
===========================
ライセンスは三条項BSDライセンスです。
詳しくは、LICENSEファイルをご覧ください。','200');
CREATE TABLE kn_author (
	id integer primary key,
	author char(256) unique
);
INSERT INTO "kn_author" VALUES(1,'name');
CREATE TABLE kn_contents_tags (
	id integer primary key,
	content_id int,
	tag_id int,
	foreign key(content_id)
		references kn_contents(id)
		on update cascade
		on delete set null,
	foreign key(tag_id)
		references kn_tags(id)
		on update cascade
		on delete restrict
);
INSERT INTO "kn_contents_tags" VALUES(1,1,1);
INSERT INTO "kn_contents_tags" VALUES(2,1,2);
CREATE TABLE kn_tags (
	id integer primary key,
	tag char(256) unique
);
INSERT INTO "kn_tags" VALUES(1,'test');
INSERT INTO "kn_tags" VALUES(2,'tast2');
CREATE TABLE kn_sites (
	id integer primary key autoincrement,
	begun date,
	updated date,
	title varchar(1024) unique not null,
	main_author_id int,
	abstract clob,
	foreign key(main_author_id)
		references kn_author(id)
		on update cascade
		on delete set null
);
INSERT INTO "kn_sites" VALUES(1,'2015-09-09 10:15:44','2015-09-09 10:15:44','kn_test_site',1,'テストページだす');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('kn_contents',1);
INSERT INTO "sqlite_sequence" VALUES('kn_sites',1);
COMMIT;
