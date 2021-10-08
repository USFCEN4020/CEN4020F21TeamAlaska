from src.Page import Page
from src.database_access import database_access as Database


# ================ MAIN ==================
# you can think of it as the driver function. It's where everything starts
def main():
    page = Page()
    page.home_page()


if __name__ == "__main__":
    # Making a connection to the database. If it doesn't already exist, it creates it
    db = Database("InCollege.sqlite3")
    main()
    db.close()
