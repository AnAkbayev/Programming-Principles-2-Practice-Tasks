
-- ==========================================
-- TSIS 1: SEARCH FUNCTION
-- ==========================================

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    contact_email VARCHAR,
    contact_birthday DATE,
    group_name VARCHAR
)
LANGUAGE sql
AS $$
    SELECT DISTINCT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g
        ON c.group_id = g.id
    LEFT JOIN phones p
        ON c.id = p.contact_id
    WHERE
        c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.name;
$$;


-- ==========================================
-- PAGINATION FUNCTION
-- ==========================================

CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    contact_email VARCHAR,
    contact_birthday DATE,
    group_name VARCHAR
)
LANGUAGE sql
AS $$
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g
        ON c.group_id = g.id
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
$$;
