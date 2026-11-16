-- ==========================================
-- TSIS 1: PHONEBOOK DATABASE
-- ==========================================

-- 1. GROUPS TABLE
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. CONTACTS TABLE
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. PHONES TABLE
CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL
        REFERENCES contacts(id)
        ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL
        CHECK (type IN ('home', 'work', 'mobile'))
);

-- ==========================================
-- INSERT DEFAULT GROUPS
-- ==========================================

INSERT INTO groups (name)
VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other');

-- ==========================================
-- INSERT SAMPLE CONTACTS
-- ==========================================

INSERT INTO contacts (name, email, birthday, group_id)
VALUES
(
    'Alex Johnson',
    'alex@gmail.com',
    '2003-05-15',
    (SELECT id FROM groups WHERE name = 'Friend')
),
(
    'John Smith',
    'john@company.com',
    '2000-10-20',
    (SELECT id FROM groups WHERE name = 'Work')
),
(
    'Sarah Wilson',
    'sarah@gmail.com',
    '2002-03-12',
    (SELECT id FROM groups WHERE name = 'Family')
),
(
    'Michael Brown',
    'michael@yahoo.com',
    '2001-07-25',
    (SELECT id FROM groups WHERE name = 'Other')
);

-- ==========================================
-- INSERT PHONE NUMBERS
-- ==========================================

INSERT INTO phones (contact_id, phone, type)
VALUES
(
    (SELECT id FROM contacts WHERE name = 'Alex Johnson'),
    '+77011234567',
    'mobile'
),
(
    (SELECT id FROM contacts WHERE name = 'Alex Johnson'),
    '+77271234567',
    'home'
),
(
    (SELECT id FROM contacts WHERE name = 'John Smith'),
    '+77029876543',
    'work'
),
(
    (SELECT id FROM contacts WHERE name = 'Sarah Wilson'),
    '+77015554433',
    'mobile'
),
(
    (SELECT id FROM contacts WHERE name = 'Michael Brown'),
    '+77017778899',
    'mobile'
);

-- ==========================================
-- CREATE INDEXES
-- ==========================================

CREATE INDEX idx_contacts_name
    ON contacts(name);

CREATE INDEX idx_contacts_email
    ON contacts(email);

CREATE INDEX idx_contacts_birthday
    ON contacts(birthday);

CREATE INDEX idx_contacts_created_at
    ON contacts(created_at);

CREATE INDEX idx_contacts_group_id
    ON contacts(group_id);

CREATE INDEX idx_phones_contact_id
    ON phones(contact_id);

CREATE INDEX idx_phones_phone
    ON phones(phone);

-- ==========================================
-- END
-- ==========================================