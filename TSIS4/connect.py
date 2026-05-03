# TSIS 3.1 saving results to database
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def save_game_result(username, score, level):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (username,))
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        player_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (player_id) 
            DO UPDATE SET 
                score = EXCLUDED.score,
                level_reached = EXCLUDED.level_reached
            WHERE EXCLUDED.score > game_sessions.score;
        """, (player_id, score, level))
        
        conn.commit()
        cur.close()
        conn.close()
   

def get_top_10():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, s.score 
            FROM game_sessions s 
            JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10;
        """)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res
    except:
        return []

def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(s.score) FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        WHERE p.username = %s;
    """, (username,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0
   