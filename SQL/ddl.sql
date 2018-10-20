use meant;

create table funding
(
  email           varchar(50)   not null,
  code            varchar(10)   not null,
  title           varchar(45)   not null,
  body            varchar(1600) not null,
  expiration      datetime      not null,
  title_img_path  varchar(100)  not null,
  cover_img_path  varchar(100)  not null,
  header_img_path varchar(500)  not null,
  primary key (email, code)
);

create table idea
(
  email varchar(50)   not null,
  code  varchar(10)   not null,
  title varchar(45)   not null,
  body  varchar(1600) not null,
  primary key (email, code)
);

create table `order`
(
  code          varchar(10) not null,
  email         varchar(50) not null,
  funding_email varchar(50) not null,
  funding_code  varchar(10) not null,
  primary key (code, email, funding_email, funding_code),
  constraint fk_order_funding1
  foreign key (funding_email, funding_code) references funding (email, code)
);

create index fk_order_funding1_idx
  on `order` (funding_email, funding_code);

create table tag
(
  title varchar(45) not null
    primary key
);

create table idea_has_tag
(
  idea_email varchar(50) not null,
  idea_code  varchar(10) not null,
  tag_title  varchar(45) not null,
  primary key (idea_email, idea_code, tag_title),
  constraint fk_idea_has_tag_idea1
  foreign key (idea_email, idea_code) references idea (email, code)
    on update cascade,
  constraint fk_idea_has_tag_tag1
  foreign key (tag_title) references tag (title)
    on update cascade
    on delete cascade
);

create index fk_idea_has_tag_idea1_idx
  on idea_has_tag (idea_email, idea_code);

create index fk_idea_has_tag_tag1_idx
  on idea_has_tag (tag_title);

create table tag_has_funding
(
  tag_title     varchar(45) not null,
  funding_email varchar(50) not null,
  funding_code  varchar(10) not null,
  primary key (tag_title, funding_email, funding_code),
  constraint fk_tag_has_funding_funding1
  foreign key (funding_email, funding_code) references funding (email, code)
    on update cascade
    on delete cascade,
  constraint fk_tag_has_funding_tag1
  foreign key (tag_title) references tag (title)
    on update cascade
);

create index fk_tag_has_funding_funding1_idx
  on tag_has_funding (funding_email, funding_code);

create index fk_tag_has_funding_tag1_idx
  on tag_has_funding (tag_title);

