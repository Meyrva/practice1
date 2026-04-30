--TSIS schema extension
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100) UNIQUE NOT NULL,
    email    VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- insert a new user by name and phone
CREATE OR REPLACE PROCEDURE upsert(p_name TEXT, p_phone TEXT, p_email TEXT, p_birthday DATE)
AS $$
DECLARE v_contact_id INT;
BEGIN 
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_name;

    IF v_contact_id IS NOT NULL THEN  
        UPDATE contacts SET email = p_email, birthday = p_birthday WHERE id = v_contact_id;
    ELSE
        INSERT INTO contacts (name, email, birthday) VALUES (p_name, p_email, p_birthday)
        RETURNING id INTO v_contact_id;
    END IF;

    IF NOT EXISTS(SELECT 1 FROM phones WHERE v_contact_id = contact_id AND phone = p_phone) 
    THEN INSERT INTO phones(contact_id,phone, type) VALUES (v_contact_id, p_phone,'mobile');
    
    END IF;
END;
$$ LANGUAGE plpgsql;


-- TSIS 3.4    1)add phone
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    SELECT id, p_phone, p_type FROM contacts WHERE name = p_contact_name;
END;
$$ LANGUAGE plpgsql;



--  insert many new users from a list
CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names TEXT[], 
    p_phones TEXT[],
    p_emails TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        
        IF length(p_phones[i]) >= 10 THEN
            CALL upsert(
                p_names[i],
                p_phone[i],
                p_email[i]
            );
        END IF;
        
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- delete data
CREATE OR REPLACE PROCEDURE delete_contact(p_ident TEXT)
AS $$
BEGIN  
    DELETE FROM contacts
    WHERE name = p_ident OR id IN(SELECT contact_id FROM phones WHERE phone = p_ident);
END;
$$ LANGUAGE plpgsql;



-- TSIS 3.4   3) Advanced Console Search & Filter
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, email VARCHAR, all_phones TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT  c.name, c.email, string_agg(p.phone, ', ')
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%' 
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.name, c.email;
END;
$$ LANGUAGE plpgsql;

-- TSIS 3.2   4) pagination
CREATE OR REPLACE FUNCTION get_advanced_contacts(
    p_group_name TEXT DEFAULT NULL,
    p_search_email TEXT DEFAULT NULL,
    p_sort_column TEXT DEFAULT 'name', 
    p_limit INT DEFAULT 10,
    p_offset INT DEFAULT 0
)
RETURNS TABLE(name VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    --TSIS 3.2   1) Filter by group and Search by email
    WHERE (p_group_name IS NULL OR g.name = p_group_name)
      AND (p_search_email IS NULL OR c.email ILIKE '%' || p_search_email || '%')
    ORDER BY 
    --Sort results
        CASE WHEN p_sort_column = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_column = 'birthday' THEN c.birthday END ASC,
        CASE WHEN p_sort_column = 'id' THEN c.id END ASC 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;


-- TSIS 3.4     2) Procedure move_to_group
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
AS $$
DECLARE
    v_group_id INT;
BEGIN
    
    INSERT INTO groups (name) 
    VALUES (p_group_name) 
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    UPDATE contacts 
    SET group_id = v_group_id
    WHERE name = p_contact_name;

    IF NOT FOUND THEN
        RAISE NOTICE 'Contact % not found.', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;