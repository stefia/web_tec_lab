create table contactrequests (
    id integer PRIMARY KEY autoincrement,
    name varchar(255) NOT NULL,
    email varchar(255),
    reqtext varchar(255),
    createdAt datetime,
    updatedAt datetime
);

create table logins (
	id integer PRIMARY KEY autoincrement,
	username varchar(255) NOT NULL UNIQUE,
	password varchar(255) NOT NULL UNIQUE
);