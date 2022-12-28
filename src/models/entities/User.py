from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, Id, Name, Apellidos, Correo, Password,Turno,Hora_inicio,Hora_final) -> None:
        self.id = Id
        self.Name = Name
        self.Apellidos = Apellidos
        self.Correo = Correo
        self.Password = Password
        self.Turno = Turno
        self.Hora = Hora_inicio
        self.Hora_final = Hora_final

    @classmethod
    def check_password(self, hashed_password, Password):
        return check_password_hash(hashed_password, Password)
