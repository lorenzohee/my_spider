create table articles(
id integer primary key not null,
title text,
content text,
article_id integer,
url_from text,
is_published integer,
articleType_id integer,
create_time datetime,
update_time datetime,
source_id integer,
num_of_view integer)
