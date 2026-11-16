
import psycopg2
import json
import csv


# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="54321",
    port=5432,
    dbname="Phonebook"
)

cursor = conn.cursor()

print("Connected to the PhonebookDB!")


# ==========================================
# CONSTANTS
# ==========================================

PHONE_TYPES = ("home", "work", "mobile")


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_group_id(group_name):

    if not group_name:
        return None

    cursor.execute("""
        INSERT INTO groups (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cursor.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    return cursor.fetchone()[0]


def print_contacts(rows):

    if not rows:
        print("\nNo contacts found.")
        return

    for row in rows:
        print("-" * 55)
        print("ID:", row[0])
        print("Name:", row[1])
        print("Email:", row[2])
        print("Birthday:", row[3])
        print("Group:", row[4])
        print("Phones:", row[5] or "No phones")


def print_search_results(rows):

    if not rows:
        print("\nNo contacts found.")
        return

    for row in rows:
        print("-" * 55)
        print("ID:", row[0])
        print("Name:", row[1])
        print("Email:", row[2])
        print("Birthday:", row[3])
        print("Group:", row[4])


def get_all_contacts():

    cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            STRING_AGG(
                p.phone || ' (' || p.type || ')',
                ', '
            )
        FROM contacts c
        LEFT JOIN groups g
            ON c.group_id = g.id
        LEFT JOIN phones p
            ON c.id = p.contact_id
        GROUP BY
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name
        ORDER BY c.id
    """)

    return cursor.fetchall()


# ==========================================
# 1. SHOW ALL CONTACTS
# ==========================================

def show_contacts():

    rows = get_all_contacts()
    print_contacts(rows)


# ==========================================
# 2. SEARCH CONTACTS
# ==========================================

def search_contacts():

    query = input("Enter name, email or phone: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    cursor.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )

    rows = cursor.fetchall()
    print_search_results(rows)


# ==========================================
# 3. FILTER BY GROUP
# ==========================================

def filter_by_group():

    group = input("Enter group name: ").strip()

    cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            STRING_AGG(
                p.phone || ' (' || p.type || ')',
                ', '
            )
        FROM contacts c
        JOIN groups g
            ON c.group_id = g.id
        LEFT JOIN phones p
            ON c.id = p.contact_id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, g.name
        ORDER BY c.name
    """, (group,))

    rows = cursor.fetchall()
    print_contacts(rows)


# ==========================================
# 4. SEARCH BY EMAIL
# ==========================================

def search_by_email():

    email = input("Enter email or part of email: ").strip()

    cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            STRING_AGG(p.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g
            ON c.group_id = g.id
        LEFT JOIN phones p
            ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, g.name
        ORDER BY c.name
    """, ('%' + email + '%',))

    rows = cursor.fetchall()
    print_contacts(rows)


# ==========================================
# 5. SORT CONTACTS
# ==========================================

def sort_contacts():

    print("""
    1. Sort by name
    2. Sort by birthday
    3. Sort by date added
    """)

    choice = input("Choose sorting option: ")

    match choice:

        case "1":
            column = "name"

        case "2":
            column = "birthday"

        case "3":
            column = "created_at"

        case _:
            print("Invalid option.")
            return

    cursor.execute(f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            STRING_AGG(p.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g
            ON c.group_id = g.id
        LEFT JOIN phones p
            ON c.id = p.contact_id
        GROUP BY c.id, g.name
        ORDER BY c.{column} NULLS LAST
    """)

    rows = cursor.fetchall()
    print_contacts(rows)


# ==========================================
# 6. PAGINATION
# ==========================================

def pagination():

    page = 0
    page_size = 3

    while True:

        cursor.execute(
            "SELECT * FROM get_contacts_page(%s, %s)",
            (page_size, page * page_size)
        )

        rows = cursor.fetchall()

        print("\n========== PAGE", page + 1, "==========")

        print_search_results(rows)

        print("""
        next - Next page
        prev - Previous page
        quit - Return to main menu
        """)

        command = input("Command: ").strip().lower()

        if command == "next":

            if len(rows) == page_size:
                page += 1
            else:
                print("You are already on the last page.")

        elif command == "prev":

            if page > 0:
                page -= 1
            else:
                print("You are already on the first page.")

        elif command == "quit":
            break

        else:
            print("Invalid command.")


# ==========================================
# 7. ADD PHONE
# ==========================================

def add_phone():

    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    phone_type = input(
        "Phone type (home/work/mobile): "
    ).strip().lower()

    if not name or not phone:
        print("Name and phone are required.")
        return

    if phone_type not in PHONE_TYPES:
        print("Invalid phone type.")
        return

    try:

        cursor.execute(
            "CALL add_phone(%s, %s, %s)",
            (name, phone, phone_type)
        )

        conn.commit()

        print("Phone added successfully!")

    except Exception as error:

        conn.rollback()
        print("Error:", error)


# ==========================================
# 8. MOVE CONTACT TO GROUP
# ==========================================

def move_to_group():

    name = input("Contact name: ").strip()
    group = input("New group name: ").strip()

    if not name or not group:
        print("Name and group are required.")
        return

    try:

        cursor.execute(
            "CALL move_to_group(%s, %s)",
            (name, group)
        )

        conn.commit()

        print("Contact moved successfully!")

    except Exception as error:

        conn.rollback()
        print("Error:", error)


# ==========================================
# 9. EXPORT TO JSON
# ==========================================

def export_json():

    cursor.execute("""
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
    """)

    contacts = cursor.fetchall()

    data = []

    for contact in contacts:

        cursor.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
        """, (contact[0],))

        phones = cursor.fetchall()

        data.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": (
                contact[3].isoformat()
                if contact[3] else None
            ),
            "group": contact[4],
            "phones": [
                {
                    "phone": phone[0],
                    "type": phone[1]
                }
                for phone in phones
            ]
        })

    with open(
        "contacts.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Export completed! File: contacts.json")


# ==========================================
# 10. IMPORT FROM JSON
# ==========================================

def import_json():

    try:

        with open(
            "contacts.json",
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON must contain a list of contacts.")

        imported = 0
        skipped = 0

        for contact in data:

            name = contact.get("name")

            if not name or not name.strip():
                print("Contact without name skipped.")
                skipped += 1
                continue

            phones = contact.get("phones", [])

            if not isinstance(phones, list):
                raise ValueError("Phones must be a list.")

            for phone in phones:
                if (
                    not phone.get("phone")
                    or phone.get("type") not in PHONE_TYPES
                ):
                    raise ValueError(
                        f"Invalid phone data for {name}"
                    )

            cursor.execute("""
                SELECT id
                FROM contacts
                WHERE LOWER(name) = LOWER(%s)
            """, (name,))

            existing = cursor.fetchone()

            if existing:

                choice = input(
                    f"\n{name} already exists.\n"
                    "Skip or overwrite? (s/o): "
                ).strip().lower()

                if choice == "s":
                    skipped += 1
                    continue

                elif choice == "o":

                    contact_id = existing[0]

                    cursor.execute("""
                        UPDATE contacts
                        SET email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE id = %s
                    """, (
                        contact.get("email"),
                        contact.get("birthday"),
                        get_group_id(contact.get("group")),
                        contact_id
                    ))

                    cursor.execute("""
                        DELETE FROM phones
                        WHERE contact_id = %s
                    """, (contact_id,))

                else:
                    print("Invalid choice. Contact skipped.")
                    skipped += 1
                    continue

            else:

                group_id = get_group_id(
                    contact.get("group")
                )

                cursor.execute("""
                    INSERT INTO contacts
                        (name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (
                    name,
                    contact.get("email"),
                    contact.get("birthday"),
                    group_id
                ))

                contact_id = cursor.fetchone()[0]

            for phone in phones:

                cursor.execute("""
                    INSERT INTO phones
                        (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (
                    contact_id,
                    phone["phone"],
                    phone["type"]
                ))

            imported += 1

        conn.commit()

        print("\nJSON import completed!")
        print("Imported/updated:", imported)
        print("Skipped:", skipped)

    except Exception as error:

        conn.rollback()
        print("JSON import error:", error)


# ==========================================
# 11. IMPORT FROM CSV
# ==========================================

def import_csv():

    try:

        with open(
            "contacts.csv",
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            required_columns = {
                "name",
                "email",
                "birthday",
                "group",
                "phone",
                "type"
            }

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                raise ValueError(
                    "CSV must contain: "
                    "name,email,birthday,group,phone,type"
                )

            imported = 0
            skipped = 0

            for row in reader:

                name = (row.get("name") or "").strip()

                if not name:
                    print("Empty name skipped.")
                    skipped += 1
                    continue

                cursor.execute("""
                    SELECT id
                    FROM contacts
                    WHERE LOWER(name) = LOWER(%s)
                """, (name,))

                if cursor.fetchone():

                    print("Duplicate skipped:", name)
                    skipped += 1
                    continue

                phone = (row.get("phone") or "").strip()
                phone_type = (row.get("type") or "").strip().lower()

                if phone and phone_type not in PHONE_TYPES:
                    raise ValueError(
                        f"Invalid phone type for {name}"
                    )

                group_id = get_group_id(
                    (row.get("group") or "").strip()
                )

                cursor.execute("""
                    INSERT INTO contacts
                        (name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (
                    name,
                    (row.get("email") or "").strip() or None,
                    (row.get("birthday") or "").strip() or None,
                    group_id
                ))

                contact_id = cursor.fetchone()[0]

                if phone:

                    cursor.execute("""
                        INSERT INTO phones
                            (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (
                        contact_id,
                        phone,
                        phone_type
                    ))

                imported += 1

        conn.commit()

        print("\nCSV import completed!")
        print("Imported:", imported)
        print("Skipped:", skipped)

    except Exception as error:

        conn.rollback()
        print("CSV import error:", error)


# ==========================================
# MAIN MENU
# ==========================================

def main():

    while True:

        print("""
================================================
                   PHONEBOOK
================================================

1.  Show all contacts
2.  Search contacts
3.  Filter contacts by group
4.  Search by email
5.  Sort contacts
6.  Navigate pages
7.  Add phone number
8.  Move contact to group
9.  Export contacts to JSON
10. Import contacts from JSON
11. Import contacts from CSV

0.  Exit

================================================
""")

        choice = input("Choose option: ").strip()

        try:

            match choice:

                case "1":
                    show_contacts()

                case "2":
                    search_contacts()

                case "3":
                    filter_by_group()

                case "4":
                    search_by_email()

                case "5":
                    sort_contacts()

                case "6":
                    pagination()

                case "7":
                    add_phone()

                case "8":
                    move_to_group()

                case "9":
                    export_json()

                case "10":
                    import_json()

                case "11":
                    import_csv()

                case "0":
                    print("Goodbye!")
                    break

                case _:
                    print("Invalid option. Try again.")

        except Exception as error:

            conn.rollback()
            print("Error:", error)

        if choice != "0":
            input("\nPress Enter to return to menu...")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nProgram interrupted.")

    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")
