CREATE TYPE goal_status AS ENUM ('active', 'completed', 'cancelled');

CREATE TABLE IF NOT EXISTS goals (
    id             BIGSERIAL     PRIMARY KEY,
    person_id      BIGINT        NOT NULL,
    account_id     BIGINT        NULL,
    name           VARCHAR(255)  NOT NULL,
    description    TEXT,
    target_amount  NUMERIC(15,2) NOT NULL,
    current_amount NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    deadline       DATE          NULL,
    status         goal_status   NOT NULL DEFAULT 'active',
    created_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_goals_person  FOREIGN KEY (person_id)  REFERENCES persons(id)  ON DELETE CASCADE,
    CONSTRAINT fk_goals_account FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE SET NULL
);

CREATE INDEX idx_goals_person        ON goals (person_id);
CREATE INDEX idx_goals_person_status ON goals (person_id, status);
