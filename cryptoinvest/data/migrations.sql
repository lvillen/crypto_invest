CREATE TABLE IF NOT EXISTS cryptos (
                                crypto_id integer PRIMARY KEY, 
                                crypto text NOT NULL);

INSERT INTO cryptos VALUES 
            (1, "EUR"), 
			(2, "ETH"), 
			(3, "LTC"), 
			(4, "BNB"), 
			(5, "EOS"),
			(6, "XLM"),
			(7, "TRX"),
			(8, "BTC"),
			(9, "XRP"),
			(10, "BCH"),
			(11, "USDT"),
			(12, "BSV"),
			(13, "ADA");

CREATE TABLE IF NOT EXISTS movements (
                                id integer PRIMARY KEY,
                                date text NOT NULL,
                                time text NOT NULL,
                                from_currency integer,
                                from_quantity real,
                                to_currency integer,
                                to_quantity real,
                                FOREIGN KEY(from_currency) REFERENCES cryptos(crypto_id),
                                FOREIGN KEY(to_currency) REFERENCES cryptos(crypto_id));