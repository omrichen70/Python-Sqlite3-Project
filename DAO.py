from ORM import orm
import DTO


class DAO:
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        # dto_type is a class, its __name__ field contains a string representing the name of the class.
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = ins_dict.values()
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})'.format(self._table_name, column_names, qmarks)
        params = list(params)
        self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)

    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()

        stmt = 'SELECT * FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        params = list(params)
        c = self._conn.cursor()
        c.execute(stmt, params)
        answer = c.fetchall()
        return answer
        # return orm(c, self._dto_type)

    def find_supplier_with_lowest_id(self, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()

        stmt = 'SELECT MIN(supplier) FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        params = list(params)
        c = self._conn.cursor()
        c.execute(stmt, params)
        answer = c.fetchone()[0]

        return answer

    def delete(self, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()

        stmt = 'DELETE FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        params = list(params)
        c = self._conn.cursor()
        c.execute(stmt, params)

    def update(self, set_values, cond):
        set_column_names = set_values.keys()
        set_params = set_values.values()

        cond_column_names = cond.keys()
        cond_params = cond.values()

        params = list(set_params) + list(cond_params)

        stmt = 'UPDATE {} SET {} WHERE {}'.format(self._table_name,
                                                  ', '.join([set + '=?' for set in set_column_names]),
                                                  ' AND '.join([cond + '=?' for cond in cond_column_names]))

        self._conn.execute(stmt, params)

    def order(self, supplier):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {} ORDER BY {}'.format(self._table_name, supplier))
        answer = c.fetchall()
        return answer