-- create table
CREATE TABLE IF NOT EXISTS phonebook2 (
    name TEXT PRIMARY KEY,
    phone TEXT NOT NULL
);
-- returns all records matching a pattern
CREATE OR REPLACE FUNCTION get_by_pattern(pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN 
    RETURN QUERY SELECT p.name, p.phone FROM phonebook2 p
                 WHERE p.name ILIKE '%' || pattern || '%' OR p.phone ILIKE '%'|| pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- queries data from the table with pagination
CREATE OR REPLACE FUNCTION get_data_with_pagination(p_limit INT, p_offset INT )
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY SELECT p.name, p.phone FROM phonebook2 p
            ORDER BY p.name 
            LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;