CREATE TYPE notification_type AS ENUM (
    'budget_exceeded',
    'budget_warning',
    'goal_reached',
    'goal_reminder'
);

CREATE TABLE IF NOT EXISTS notifications (
    id         BIGSERIAL         PRIMARY KEY,
    person_id  BIGINT            NOT NULL,
    type       notification_type NOT NULL,
    title      VARCHAR(255)      NOT NULL,
    message    TEXT              NOT NULL,
    is_read    BOOLEAN           NOT NULL DEFAULT FALSE,
    budget_id  BIGINT            NULL,
    goal_id    BIGINT            NULL,
    created_at TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notif_person FOREIGN KEY (person_id) REFERENCES persons(id)  ON DELETE CASCADE,
    CONSTRAINT fk_notif_budget FOREIGN KEY (budget_id) REFERENCES budgets(id)  ON DELETE SET NULL,
    CONSTRAINT fk_notif_goal   FOREIGN KEY (goal_id)   REFERENCES goals(id)    ON DELETE SET NULL
);

CREATE INDEX idx_notif_person         ON notifications (person_id);
CREATE INDEX idx_notif_person_unread  ON notifications (person_id, is_read);
CREATE INDEX idx_notif_person_created ON notifications (person_id, created_at);
