create table articles(
id integer primary key not null,
title text,
content text,
article_id integer,
url_from text,
is_published integer,
articleType_id integer,
created_at datetime)
