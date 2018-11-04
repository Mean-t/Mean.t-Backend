drop schema meant;
create schema meant;
use meant;

create table funding
(
  funding_id       int unsigned                       not null,
  email            varchar(50)                        not null,
  code             varchar(10)                        not null,
  title            varchar(45)                        null,
  body             varchar(1600)                      null,
  expiration       datetime                           null,
  title_img_path   varchar(100)                       null,
  cover_img_path   varchar(100)                       null,
  header_img_paths varchar(500)                       null,
  host             varchar(10)                        null,
  created_at       datetime default CURRENT_TIMESTAMP not null,
  updated_at       datetime default CURRENT_TIMESTAMP not null,
  primary key (funding_id, email, code),
  constraint index_UNIQUE
  unique (funding_id)
);

create table funding_status
(
  funding_funding_id int unsigned                                         not null,
  funding_email      varchar(50)                                          not null,
  funding_code       varchar(10)                                          not null,
  balance            int unsigned default '0'                             not null,
  participants_num   int unsigned default '0'                             not null,
  status             enum ('ready', 'success', 'manufacture', 'complete') null,
  primary key (funding_funding_id, funding_email, funding_code),
  constraint fk_funding_status_funding1
  foreign key (funding_funding_id, funding_email, funding_code) references funding (funding_id, email, code)
    on update cascade
    on delete cascade
);

create table idea
(
  idea_id    int unsigned auto_increment,
  email      varchar(50)                        not null,
  code       varchar(10)                        not null,
  title      varchar(45)                        null,
  body       varchar(1600)                      null,
  created_at datetime default CURRENT_TIMESTAMP not null,
  updated_at datetime default CURRENT_TIMESTAMP not null,
  primary key (idea_id, email, code)
);

create table funding_has_idea
(
  funding_funding_id int unsigned not null,
  funding_email      varchar(50)  not null,
  funding_code       varchar(10)  not null,
  idea_idea_id       int unsigned not null,
  idea_email         varchar(50)  not null,
  idea_code          varchar(10)  not null,
  primary key (funding_funding_id, funding_email, funding_code, idea_idea_id, idea_email, idea_code),
  constraint fk_funding_has_idea_funding1
  foreign key (funding_funding_id, funding_email, funding_code) references funding (funding_id, email, code)
    on update cascade
    on delete cascade,
  constraint fk_funding_has_idea_idea1
  foreign key (idea_idea_id, idea_email, idea_code) references idea (idea_id, email, code)
    on update cascade
);

create index fk_funding_has_idea_funding1_idx
  on funding_has_idea (funding_funding_id, funding_email, funding_code);

create index fk_funding_has_idea_idea1_idx
  on funding_has_idea (idea_idea_id, idea_email, idea_code);

create table `order`
(
  code               varchar(10)                                                                                not null,
  email              varchar(50)                                                                                not null,
  payee              varchar(10)                                                                                not null,
  destination        varchar(50)                                                                                not null,
  status             enum ('cancel', 'standby', 'ready', 'manufacture', 'delivery', 'arrive') default 'standby' not null,
  ordered_at         datetime default CURRENT_TIMESTAMP                                                         not null,
  funding_funding_id int unsigned                                                                               not null,
  funding_email      varchar(50)                                                                                not null,
  funding_code       varchar(10)                                                                                not null,
  primary key (code, email, funding_funding_id, funding_email, funding_code),
  constraint fk_order_funding1
  foreign key (funding_funding_id, funding_email, funding_code) references funding (funding_id, email, code)
);

create index fk_order_funding1_idx
  on `order` (funding_funding_id, funding_email, funding_code);

create table tag
(
  title varchar(45) not null
    primary key
);

create table funding_has_tag
(
  funding_funding_id int unsigned not null,
  funding_email      varchar(50)  not null,
  funding_code       varchar(10)  not null,
  tag_title          varchar(45)  not null,
  primary key (funding_funding_id, funding_email, funding_code, tag_title),
  constraint fk_funding_has_tag_funding1
  foreign key (funding_funding_id, funding_email, funding_code) references funding (funding_id, email, code)
    on update cascade,
  constraint fk_funding_has_tag_tag1
  foreign key (tag_title) references tag (title)
);

create index fk_funding_has_tag_funding1_idx
  on funding_has_tag (funding_funding_id, funding_email, funding_code);

create index fk_funding_has_tag_tag1_idx
  on funding_has_tag (tag_title);

create table idea_has_tag
(
  idea_idea_id int unsigned not null,
  idea_email   varchar(50)  not null,
  idea_code    varchar(10)  not null,
  tag_title    varchar(45)  not null,
  primary key (idea_idea_id, idea_email, idea_code, tag_title),
  constraint fk_idea_has_tag_idea1
  foreign key (idea_idea_id, idea_email, idea_code) references idea (idea_id, email, code)
    on update cascade,
  constraint fk_idea_has_tag_tag1
  foreign key (tag_title) references tag (title)
);

create index fk_idea_has_tag_idea1_idx
  on idea_has_tag (idea_idea_id, idea_email, idea_code);

create index fk_idea_has_tag_tag1_idx
  on idea_has_tag (tag_title);

