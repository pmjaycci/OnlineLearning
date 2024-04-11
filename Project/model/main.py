from model.database import Database


class Main:
    def learn_load():
        sql = f'SELECT * FROM online_learn'

        rows = Database.read_all_db(sql)

        return rows if rows is not None else []

    def search_learn():
        # TODO: 검색기능 추가해야함
        return
