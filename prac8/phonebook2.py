# phonebook.py
import psycopg2
from connect import get_connection

def load_sql_scripts():
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
                with open('functions.sql', 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
                with open('procedures.sql', 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
        conn.commit()
    conn.close()

def print_contacts(rows):
    for row in rows:
        print(f"| {row[0]:<15} | {row[1]:<13} |")
    print(f"{'-'*35}\n")

def main():
    while True:
        print("\nPhoneBook")
        print("1. show contacts")
        print("2. upsert")
        print("3. insert")
        print("4. find")
        print("5. delete")
        print("0. exit")

        choice = input("\nChoice: ")

        conn = get_connection()
        if not conn:
            continue

        try:
            with conn.cursor() as cur:
                if choice == "1":
                    limit = int(input("How many contacts to show (LIMIT): "))
                    offset = int(input("How many contacts to skip (OFFSET): "))
 
                    cur.execute("SELECT * FROM get_data_with_pagination(%s, %s)", (limit, offset))
                    print_contacts(cur.fetchall())

                elif choice == "2":
                    name = input("name: ")
                    phone = input("phone: ")
                 
                    cur.execute("CALL upsert(%s, %s)", (name, phone))
                    conn.commit()
                    print(f"contact {name} saved.")

                elif choice == "3":
                 
                    names = ['Alibi', 'Ivan', 'Bob', 'Alice']
                    phones = ['87071112233', '87015781223', '87779998877', '87030019832']
                    print(list(zip(names, phones)))
                    
                 
                    cur.execute("CALL insert_many_users(%s, %s, %s, %s, %s)", (names, phones, [], [], []))
                    conn.commit()
                    
                
                    print("All data has been uploaded successfully")

                elif choice == "4":
                    pattern = input("looking for a part of a name or phone number: ")
                
                    cur.execute("SELECT * FROM get_by_pattern(%s)", (pattern,))
                    print_contacts(cur.fetchall())

                elif choice == "5":
                    identifier = input("Enter a Name or Phone Number to delete: ")
                   
                    cur.execute("CALL delete_contact(%s)", (identifier,))
                    conn.commit()
                    print("Deletion completed")

                elif choice == "0":
                    break
                else:
                    print("incorrect choice")
        finally:
            conn.close()

if __name__ == "__main__":
    load_sql_scripts() 
    main()