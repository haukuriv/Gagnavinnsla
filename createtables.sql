drop table link_power;
drop table powers;
drop table fights;
drop table supers;
-- \i C:/Users/Lenovo/Desktop/Gagnavinnsla/Hopverkefni/createtables.sql


CREATE TABLE supers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),

    publisher VARCHAR(50),

    gender VARCHAR(7),
    weight INT,
    height INT,
    race VARCHAR(50),
    eye_color VARCHAR(50),
    hair_color VARCHAR(50),
    skin_color VARCHAR(50),

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
    super1_id INT REFERENCES supers (id),
    super2_id INT REFERENCES supers (id),
    wins1 INT,
    wins2 INT,
    tie INT
);

CREATE TABLE powers (
    id SERIAL PRIMARY KEY,
    power VARCHAR(250)
);

CREATE TABLE link_power (
    id SERIAL PRIMARY KEY,
    super_id INT REFERENCES supers(id),
    power_id INT REFERENCES powers(id)
);