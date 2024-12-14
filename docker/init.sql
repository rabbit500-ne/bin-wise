CREATE TABLE municipalities (
    municipality_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE item_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE municipality_itemtype_category_map (
    municipality_id INTEGER REFERENCES municipalities(municipality_id),
    type_id INTEGER REFERENCES item_types(type_id),
    category_id INTEGER REFERENCES categories(category_id),
    PRIMARY KEY (municipality_id, type_id)
);

CREATE TABLE municipality_category_instructions (
    instruction_id SERIAL PRIMARY KEY,
    municipality_id INTEGER REFERENCES municipalities(municipality_id),
    category_id INTEGER REFERENCES categories(category_id),
    instruction_text TEXT NOT NULL
);
