import psycopg2


class User:
    def __init__(self, user_id=None, name: str = None, email: str = None):
        self.user_id = user_id
        self.name = name
        self.email = email

    @staticmethod
    def _connect():
        return psycopg2.connect(
            host='localhost',
            database='jamoliddin',
            user='postgres',
            password='0707',
            port='5433'
        )

    @staticmethod
    def create_table():
        with User._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE members (
                    user_id     SERIAL PRIMARY KEY,
                    name        VARCHAR(100) NOT NULL,
                    email       VARCHAR(100) NOT NULL UNIQUE
                )
            ''')
            conn.commit()
            cursor.close()

    def save(self):
        with User._connect() as conn:
            cursor = conn.cursor()
            if self.user_id:
                cursor.execute('''
                    UPDATE members
                    SET name = %s, email = %s
                    WHERE user_id = %s
                ''', (self.name, self.email, self.user_id))
            else:
                cursor.execute('''
                    INSERT INTO members (name, email)
                    VALUES (%s, %s)
                    RETURNING user_id
                ''', (self.name, self.email))
                self.user_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()

    @staticmethod
    def get_users():
        with User._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id, name, email FROM members')
            users = cursor.fetchall()
            cursor.close()
            return [User(user_id, name, email) for user_id, name, email in users]

    @staticmethod
    def get_user(user_id):
        with User._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id, name, email FROM members WHERE user_id = %s',
                           (user_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return User(row[0], row[1], row[2])
            return None

    @staticmethod
    def delete_user(user_id):
        with User._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM members WHERE user_id = %s', (user_id,))
            conn.commit()
            cursor.close()

    def update_user(self, name: str, email: str):
        if name:
            self.name = name
        if email:
            self.email = email
        self.save()


if __name__ == "__main__":

    user1 = User(name='Jamoliddin', email='jamoliddin123@gmail.com')
    user1.save()

    user_list = User.get_users()
    for user in user_list:
        print(user.user_id, user.name, user.email)

    user = User.get_user(user1.user_id)
    if user:
        print(user.user_id, user.name, user.email)

    user1.update_user(name='Jamoliddinbek', email='jmld123@gmail.com')

    User.delete_user(user1.user_id)
