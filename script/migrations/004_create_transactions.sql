CREATE TYPE transaction_type AS ENUM ('income', 'expense');

CREATE TABLE IF NOT EXISTS transactions (
    id               BIGSERIAL        PRIMARY KEY,
    account_id       BIGINT           NOT NULL,
    category_id      BIGINT           NOT NULL,
    store            VARCHAR(255)     NOT NULL,
    amount           NUMERIC(15,2)    NOT NULL,
    type             transaction_type NOT NULL DEFAULT 'expense',
    transaction_date DATE             NOT NULL,
    description      TEXT,
    created_at       TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tx_account  FOREIGN KEY (account_id)  REFERENCES accounts(id)   ON DELETE CASCADE,
    CONSTRAINT fk_tx_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

CREATE INDEX idx_tx_account   ON transactions (account_id);
CREATE INDEX idx_tx_category  ON transactions (category_id);
CREATE INDEX idx_tx_date      ON transactions (transaction_date);
CREATE INDEX idx_tx_acct_date ON transactions (account_id, transaction_date);
