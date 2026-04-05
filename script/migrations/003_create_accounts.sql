CREATE TYPE account_type AS ENUM ('checking', 'savings', 'credit', 'cash');

CREATE TABLE IF NOT EXISTS accounts (
    id         BIGSERIAL     PRIMARY KEY,
    person_id  BIGINT        NOT NULL,
    name       VARCHAR(255)  NOT NULL,
    type       account_type  NOT NULL DEFAULT 'checking',
    currency   CHAR(3)       NOT NULL DEFAULT 'RUB',
    balance    NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_accounts_person FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
);

CREATE INDEX idx_accounts_person ON accounts (person_id);
