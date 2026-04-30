import psycopg2, csv, json
from connect import get_connection

def load_sql_scripts():
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            with open('procedures.sql', 'r', encoding='utf-8') as f:
                cur.execute(f.read())
        conn.commit()
        conn.close()

def print_contacts(rows):
    for row in rows:
        print(f"| {row[0]:<15} | {row[1]:<20} | {row[2] } |")
    print(f"{'-'*60}\n")


#TSIS 3.3    1) Export to JSON
def export_to_json(conn): 
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name, array_agg(p.phone)
            FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
            """)
        rows = cur.fetchall()
        data = [{"name": r[0], "email": r[1], "birthday": str(r[2]), "group": r[3], "phones": r[4]} for r in rows]
        
        with open('contacts.json', 'w') as f:
            json.dump(data, f, indent=4)
    print("Exported to contacts.json")

# TSIS 3.3    2)Import from JSON
def import_from_json(conn, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with conn.cursor() as cur:
            for entry in data:
                
                cur.execute("SELECT id FROM contacts WHERE name = %s", (entry['name'],))
                exists = cur.fetchone()
                
                if exists:
                    print(f"\nContact '{entry['name']}' already exists.")
                    u_choice = input("Skip or Overwrite? (s/o): ").lower()
                    if u_choice == 's':
                        continue
                
                main_phone = entry['phones'][0] if (entry.get('phones') and entry['phones']) else None
                
                birthday = entry.get('birthday')
                if birthday == "None" or birthday == "":
                    birthday = None
                cur.execute("CALL upsert(%s, %s, %s, %s)", 
                            (entry['name'], main_phone, entry.get('email'),birthday))
        conn.commit()
        print(f"Imported from {filename}")
    except FileNotFoundError:
        print("Error: JSON file not found.")


# TSIS 3.3     2) Extend CSV import
def import_from_csv(conn, filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        with conn.cursor() as cur:
            for row in reader:
                cur.execute("CALL upsert(%s, %s, %s, %s)", (row['name'], row['phone'], row.get('email'), row.get('birthday')))
        conn.commit()
    print(f"Imported from {filename}")



def main():
    while True:
        print("\nPhoneBook")
        print("1. show contacts")
        print("2. upsert")
        print("3. import from CSV")
        print("4. find")
        print("5. delete")
        print("6. export to JSON")
        print("7. move to group")
        print("8. import from JSON")
        print("0. exit")

        choice = input("\nChoice: ")

        conn = get_connection()
        if not conn:
            continue

        try:
            with conn.cursor() as cur:
                if choice == "1":
                    # ask for the filtering and sorting parameters
                    group_filter = input("Filter by group (leave empty for all): ") or None
                    email_search = input("Search by email (leave empty for all): ") or None
                    
                    print("Sort by: 1. Name, 2. Birthday, 3. Date Added")
                    sort_choice = input("Choice: ")
                    sort_map = {"1": "name", "2": "birthday", "3": "id"}
                    sort_col = sort_map.get(sort_choice, "name")

                    page = 0
                    limit = 5
                    
                    while True:
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT * FROM get_advanced_contacts(%s, %s, %s, %s, %s)
                            """, (group_filter, email_search, sort_col, limit, page * limit))
                            
                            rows = cur.fetchall()
                            
                            if not rows and page == 0:
                                print("No contacts found.")
                                break
                            
                         
                            print(f"\n--- Page {page + 1} ---")
                            for r in rows:
                                print(f"Name: {r[0]} | Email: {r[1]} | B-day: {r[2]} | Group: {r[3]}")
                            
                            # TSIS 3.2  console loop that lets the user navigate
                            nav = input("\n[n] next, [p] prev, [q] quit: ").lower()
                            if nav == 'n':
                                if len(rows) == limit: page += 1
                                else: print("Last page reached.")
                            elif nav == 'p':
                                page = max(0, page - 1)
                            else:
                                break

                elif choice == "2":
                    name = input("name: ")
                    phone = input("phone: ")
                    email = input("email: ") or None
                    birthday = input("birthday (YYYY-MM-DD) or empty: ") or None

                    cur.execute("CALL upsert(%s, %s, %s, %s)", (name, phone, email,birthday))
                    conn.commit()
                    print(f"contact {name} saved.")

                elif choice == "3":
                    import_from_csv(conn, 'contacts.csv')
                    print("All data has been uploaded successfully")

                elif choice == "4":
                    pattern = input("looking for a part of a name/email/number: ")
                
                    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
                    rows = cur.fetchall()
                    for row in rows:
                        print(f"Name: {row[0]} | Email: {row[1]} | Phone: {row[2]}")

                elif choice == "5":
                    identifier = input("Enter a Name or Phone Number to delete: ")
                   
                    cur.execute("CALL delete_contact(%s)", (identifier,))
                    conn.commit()
                    print("Deletion completed")

                elif choice == "6":
                    export_to_json(conn)

                elif choice == "7":
                    c_name = input("Enter contact name: ")
                    g_name = input("Enter new group name: ")
                    cur.execute("CALL move_to_group(%s, %s)", (c_name, g_name))
                    conn.commit()
                    print(f"Contact {c_name} successfully moved to group '{g_name}'.")
                
                elif choice == "8": 
                    import_from_json(conn, 'contacts.json' )
                elif choice == "0":
                    break
                else:
                    print("incorrect choice")
        finally:
            conn.close()

if __name__ == "__main__":
    load_sql_scripts() 
    main()