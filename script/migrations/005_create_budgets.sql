CREATE TABLE IF NOT EXISTS budgets (
    id           BIGSERIAL     PRIMARY KEY,
    person_id    BIGINT        NOT NULL,
    category_id  BIGINT        NOT NULL,
    amount       NUMERIC(15,2) NOT NULL,
    period_year  SMALLINT      NOT NULL,
    period_month SMALLINT      NOT NULL CHECK (period_month BETWEEN 1 AND 12),
    created_at   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_budgets_person   FOREIGN KEY (person_id)   REFERENCES persons(id)    ON DELETE CASCADE,
    CONSTRAINT fk_budgets_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    CONSTRAINT uq_budget_person_cat_period UNIQUE (person_id, category_id, period_year, period_month)
);

CREATE INDEX idx_budgets_person        ON budgets (person_id);
CREATE INDEX idx_budgets_person_period ON budgets (person_id, period_year, period_month);
