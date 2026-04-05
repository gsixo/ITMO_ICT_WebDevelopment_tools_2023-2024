CREATE TYPE category_type AS ENUM ('income', 'expense', 'both');

CREATE TABLE IF NOT EXISTS categories (
    id        BIGSERIAL     PRIMARY KEY,
    name      VARCHAR(100)  NOT NULL,
    icon      VARCHAR(50),
    color     VARCHAR(7),
    type      category_type NOT NULL DEFAULT 'expense',
    is_system BOOLEAN       NOT NULL DEFAULT FALSE
);

INSERT INTO categories (name, icon, color, type, is_system) VALUES
    ('Food & Groceries', 'shopping-cart',   '#4CAF50', 'expense', TRUE),
    ('Transport',        'car',             '#2196F3', 'expense', TRUE),
    ('Entertainment',    'film',            '#9C27B0', 'expense', TRUE),
    ('Health',           'heart',           '#F44336', 'expense', TRUE),
    ('Utilities',        'zap',             '#FF9800', 'expense', TRUE),
    ('Shopping',         'bag',             '#00BCD4', 'expense', TRUE),
    ('Salary',           'briefcase',       '#8BC34A', 'income',  TRUE),
    ('Freelance',        'trending-up',     '#009688', 'income',  TRUE),
    ('Investment',       'bar-chart',       '#3F51B5', 'income',  TRUE),
    ('Other',            'more-horizontal', '#9E9E9E', 'both',    TRUE);
