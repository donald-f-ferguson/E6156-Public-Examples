#
# The wisdom of ChatGPT
#
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        print(f"Connecting to database with connection string: {self.connection_string}")
        # Actual database connection logic would go here

    def disconnect(self):
        print("Disconnecting from the database")
        # Actual database disconnection logic would go here


class UserService:
    def __init__(self, database):
        self.database = database

    def get_user(self, user_id):
        self.database.connect()
        # Logic to fetch user from the database based on user_id would go here
        print(f"Fetching user with ID {user_id}")
        self.database.disconnect()


def main():
    # Dependency injection: Creating instances of dependencies and injecting them into the service
    db = Database("mysql://user:password@localhost:3306/mydatabase")
    user_service = UserService(db)

    # Using the service
    user_service.get_user(1)


if __name__ == "__main__":
    main()
