from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, admin):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID, Name, Apellidos, Correo, Password, Turno, Hora, Hora_final FROM admin WHERE Correo = '{}'""".format(admin.Correo)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                admin = User(row[0],row[1],row[2],row[3], User.check_password(row[4], admin.Password),row[5],row[6],row[7])
                return admin
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID, Name, Apellidos, Correo, Password, Turno, Hora, Hora_final FROM admin WHERE ID = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)