-- insert a new user by name and phone
CREATE OR REPLACE PROCEDURE upsert(p_name TEXT, p_phone TEXT)
AS $$
BEGIN 
    IF EXISTS (SELECT 1 FROM phonebook2 WHERE name = p_name) THEN
        UPDATE phonebook2 SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook2 (name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

--  insert many new users from a list
CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names TEXT[], 
    p_phones TEXT[],
    INOUT out_bad_names TEXT[] DEFAULT '{}',
    INOUT out_bad_phones TEXT[] DEFAULT '{}',
    INOUT out_reasons TEXT[] DEFAULT '{}'
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        
        IF length(p_phones[i]) < 10 THEN
            out_bad_names := array_append(out_bad_names, p_names[i]);
            out_bad_phones := array_append(out_bad_phones, p_phones[i]);
            out_reasons := array_append(out_reasons, 'Телефон короче 10 символов');
        ELSE
            
            IF EXISTS (SELECT 1 FROM phonebook2 WHERE name = p_names[i]) THEN
                UPDATE phonebook2 SET phone = p_phones[i] WHERE name = p_names[i];
            ELSE
                INSERT INTO phonebook2 (name, phone) VALUES (p_names[i], p_phones[i]);
            END IF;
        END IF;
        
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- delete data
CREATE OR REPLACE PROCEDURE delete_contact(p_ident TEXT)
AS $$
BEGIN  
    DELETE FROM phonebook2
    WHERE name = p_ident OR phone = p_ident;
END;
$$ LANGUAGE plpgsql;
