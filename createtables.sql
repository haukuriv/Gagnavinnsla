drop table powers;
drop table link_power;
drop table fights;
drop table supers;
-- \i C:/Users/Lenovo/Desktop/Gagnavinnsla/Hopverkefni/createtables.sql


CREATE TABLE supers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),

    publisher VARCHAR(50),

    gender CHAR(1),
    weight INT,
    height INT,

    alignment VARCHAR(7),

    combat INT,
    durability INT,
    intelligence INT,
    power INT,
    speed INT,
    strength INT
);

CREATE TABLE fights (
    id SERIAL PRIMARY KEY,
    super1 INT REFERENCES supers (id),
    super2 INT REFERENCES supers (id),
    wins1 INT,
    wins2 INT,
    tie INT
);

CREATE TABLE powers (
    id serial PRIMARY KEY,
    power VARCHAR(250)
);

CREATE TABLE link_power ( 
    id serial PRIMARY KEY,
    hero_id serial REFERENCES supers(id),
    power_id serial REFERENCES powers(id)
);


