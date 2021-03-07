CREATE TABLE IF NOT EXISTS tb_products (
    id SERIAL NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (product_name)
);

CREATE TABLE IF NOT EXISTS tb_genres (
    id SERIAL NOT NULL,
    genre_name VARCHAR(120) NOT NULL,
    UNIQUE (genre_name),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS tb_states (
    id SERIAL NOT NULL,
    state_name VARCHAR(75) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (state_name)
);

CREATE TABLE IF NOT EXISTS tb_cities (
    id SERIAL NOT NULL,
    city_name VARCHAR(120) NOT NULL,
    id_state INTEGER NOT NULL,
    UNIQUE (city_name, id_state),
    PRIMARY KEY (id),
    FOREIGN KEY (id_state) REFERENCES tb_states(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tb_costumers (
    id SERIAL NOT NULL,
    id_city INTEGER NOT NULL,
    id_genre INTEGER NOT NULL,
    uuid UUID NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    birth_date date NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(255),
    address VARCHAR(255) NOT NULL,
    postal_code VARCHAR(8),
    complement VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE (cpf),
    UNIQUE (uuid),
    FOREIGN KEY (id_city) REFERENCES tb_cities(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_genre) REFERENCES tb_genres(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tb_orders (
    id SERIAL NOT NULL,
    id_costumer INTEGER NOT NULL,
    discount INTEGER NOT NULL DEFAULT 0 CHECK(discount >= 0 AND discount <= 100),
    order_date TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (id_costumer) REFERENCES tb_costumers(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tb_order_details (
    id_order INTEGER NOT NULL,
    id_product INTEGER NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (id_order, id_product),
    FOREIGN KEY (id_order) REFERENCES tb_orders(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_product) REFERENCES tb_products(id) ON UPDATE CASCADE ON DELETE CASCADE
);
