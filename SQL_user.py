import re
from sqlalchemy import create_engine, text
import pandas as pd
import json




class SQL_user:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    password_regex = r'^(?=.*[a-zàâäéèêëîïôöùûüÿçáéíñóúü])(?=.*[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇÁÉÍÑÓÚÜ])(?=.*\d)(?=.*[@$!%*?&_\"\'\'])[A-Za-zàâäéèêëîïôöùûüÿçáéíñóúüÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇÁÉÍÑÓÚÜ\d@$!%*?&_\"\'\']{8,}$'
    # Charger les informations de connexion depuis le fichier JSON
    with open("db_identificator.json", "r") as file:
        config = json.load(file)

    # Informations de connexion
    DATABASE_TYPE = config['DATABASE_TYPE']
    DBAPI = config['DBAPI']
    HOST = config['HOST']
    PORT = config['PORT']
    USER = config['USER']
    PASSWORD = config['PASSWORD']
    DATABASE = config['DATABASE']


    def __init__(self):
        self.engine = create_engine(f"{SQL_user.DATABASE_TYPE}+{SQL_user.DBAPI}://{SQL_user.USER}:{SQL_user.PASSWORD}@{SQL_user.HOST}:{SQL_user.PORT}/{SQL_user.DATABASE}")

    def is_email_known(self, email):
        query = text('SELECT COUNT(*) FROM "user" WHERE email = :email')
        with self.engine.connect() as connection:
            result = connection.execute(query, {'email': email})
            count = result.scalar()
        return count > 0
    
    def is_authentificate(self, email, password):
        query = text('SELECT COUNT(*) FROM "user" WHERE email = :email and password = :password')
        with self.engine.connect() as connection:
            result = connection.execute(query, {'email': email, 'password': password})
            count = result.scalar()
        return count > 0

    @staticmethod
    def is_valid_email(email):
        return re.match(SQL_user.email_regex, email) is not None

    @staticmethod
    def is_valid_password(password):
        return re.match(SQL_user.password_regex, password) is not None

    @staticmethod
    def is_valid_name(name):
        return bool(name) and all(char.isalpha() or char.isspace() for char in name)

    @staticmethod
    def is_valid_lastname(lastname):
        return bool(lastname) and all(char.isalpha() or char.isspace() for char in lastname)

    def validate_user(self, email, password, name, lastname):
        if not self.is_valid_email(email):
            print("Mail invalide")
            return False
        if not self.is_valid_password(password):
            print("Mot de passe invalide merci de renseigner minimum 8 caractères dont un chiffre, majuscule et symbole")
            return False
        if not self.is_valid_name(name):
            print("Name invalid")
            return False
        if not self.is_valid_lastname(lastname):
            print("Lastname invalid")
            return False
        return True
    

    # alternatif
    def val(self, email, password, name, lastname):
        return not self.is_valid_email(email) and not self.is_valid_password(password) and not self.is_valid_name(name) and not self.is_valid_lastname(lastname)


    def add_user(self,email, password, name, lastname):
        dict_user = {'first_name': [name], 'last_name': [lastname], 'email': [email], 'password': [password]}
        df_user = pd.DataFrame(dict_user)
        df_user.to_sql(name='user', con=self.engine, if_exists = 'append', index=False)