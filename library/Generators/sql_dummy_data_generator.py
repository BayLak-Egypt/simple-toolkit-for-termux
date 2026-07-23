import secrets
import color

DESCRIPTION = "SQL INSERT Statements Generator for DB Testing"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

FIRST_NAMES = ["Ahmed", "Sara", "Omar", "Mona", "Khaled", "Laila", "Youssef", "Nour"]
LAST_NAMES = ["Hassan", "Ali", "Ibrahim", "Mahmoud", "Khalil", "Mostafa", "Ghanem"]
DOMAINS = ["example.com", "test.org", "demo.net"]

def generate_sql_insert(table_name: str, count: int = 5) -> str:
    """Generate SQL INSERT statements with randomized mock user data."""
    statements = []
    for _ in range(count):
        fname = secrets.choice(FIRST_NAMES)
        lname = secrets.choice(LAST_NAMES)
        email = f"{fname.lower()}.{lname.lower()}{secrets.randbelow(99)}@{secrets.choice(DOMAINS)}"
        age = secrets.randbelow(40) + 18
        
        sql = f"INSERT INTO {table_name} (first_name, last_name, email, age) VALUES ('{fname}', '{lname}', '{email}', {age});"
        statements.append(sql)
    
    return "\n".join(statements)

def run():
    print(color.color_text("--- SQL INSERT Statement Generator ---", COLOR))
    
    table_name = input("Enter target table name (default 'users'): ").strip() or "users"
    
    try:
        count = int(input("How many rows/statements to generate? (default 5): ").strip() or "5")
        if count < 1:
            count = 5
    except ValueError:
        count = 5

    sql_output = generate_sql_insert(table_name, count)

    print(color.color_text(f"\n[+] Generated SQL Statements:\n", color.GREEN))
    print(sql_output)
