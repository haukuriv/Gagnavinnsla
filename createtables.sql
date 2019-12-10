DROP TABLE fights;
DROP TABLE CosmicEntity;
DROP TABLE publishers;
DROP TABLE alignments;

-- \i C:/Users/Lenovo/Desktop/Gagnavinnsla/Hopverkefni/createtables.sql


CREATE TABLE alignments (
    alignment VARCHAR(7) PRIMARY KEY
);

CREATE TABLE publishers (
    publisher VARCHAR(50) PRIMARY KEY
);

CREATE TABLE CosmicEntity (
    name VARCHAR(50) PRIMARY KEY,

    publisher VARCHAR(50) REFERENCES publishers (publisher),

    gender CHAR(1),
    weight INT,
    height INT,

    alignment VARCHAR(7) REFERENCES alignments (alignment),

    combat INT,
    durability INT,
    intelligence INT,
    power INT,
    speed INT,
    strength INT
);

CREATE TABLE fights (
    id SERIAL PRIMARY KEY,
    hero1 VARCHAR (50) REFERENCES CosmicEntity (name),
    hero2 VARCHAR (50) REFERENCES CosmicEntity (name),
    wins1 INT,
    wins2 INT,
    tie INT
);