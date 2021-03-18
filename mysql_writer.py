"""
Project: Data-Mining GOG (Good Old Games)
MySQL CLASS - inserting and updating results into DB.
"""
import mysql.connector
import config
from datetime import datetime


class WebsiteDB:
    def __init__(self, list_of_games_data):
        self._data = list_of_games_data
        self._conn = self.__connect_to_db(config)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()

    def __connect_to_db(self, config):
        return mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE
        )

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def write_game_titles(self):
        """Writes to title table"""
        for dicto in self._data:  # todo: change dicto name
            try:
                sql = """INSERT INTO game_titles
                             (  title_sku,
                                title_name,
                                title_release_date,
                                title_supported_os,
                                title_company,
                                title_size_mb,
                                title_url)
                              VALUES(%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            title_name = VALUES(title_name),
                            title_release_date = VALUES(title_release_date),
                            title_supported_os = VALUES(title_supported_os),
                            title_company = VALUES(title_company),
                            title_size_mb = VALUES(title_size_mb),
                            title_url = VALUES(title_url)
                        """
                val = (dicto[config.keyname_game_sku],
                       dicto[config.keyname_game_title],
                       dicto[config.keyname_release_date],
                       dicto[config.keyname_works_on],
                       ', '.join(set(dicto[config.keyname_company])),
                       dicto[config.keyname_game_size],
                       dicto[config.keyname_game_url])
                self.cursor.execute(sql, val)
            except Exception:
                pass

    def write_game_genres(self):
        """Write into game_genres the genres of the game.
        Each game could have at 3 different types of genres => each one in a row
        """
        for dicto in self._data:  # todo: change dicto name
            for genere_name in dicto[config.keyname_genre]:
                try:
                    sql = """INSERT INTO game_genres (title_sku, genre_name) VALUES(%s,%s) 
                             ON DUPLICATE KEY UPDATE 
                                genre_name = VALUES(genre_name)             
                            """
                    val = (
                    dicto[config.keyname_game_sku], genere_name)
                    self.cursor.execute(sql, val)
                except Exception:
                    pass

    def write_game_prices(self):
        """Writes to game_prices"""
        for dicto in self._data:  # todo: change dicto name
            try:
                sql = """INSERT INTO game_prices
                             (title_sku, 
                             price_quote_datetime, 
                             price_base, 
                             price_final, 
                             discount) 
                        VALUES(%s,%s,%s,%s,%s)           
                        """
                val = (dicto[config.keyname_game_sku],
                       datetime.now().strftime(config.DATETIME_FORMAT),
                       dicto[config.keyname_game_base_price],
                       dicto[config.keyname_gmae_final_price],
                       dicto[config.keyname_game_discount]
                       )
                self.cursor.execute(sql, val)
            except Exception:
                pass

    def write_game_scores(self):
        """Writes into game_scores tbl (sql db).
           Each row is a quote of the score for the script running time.
        """
        for dicto in self._data:  # todo: change dicto name
            try:
                sql = """INSERT INTO game_scores
                             (title_sku, 
                             score_quote_datetime,
                             score)
                        VALUES(%s,%s,%s)           
                        """
                val = (dicto[config.keyname_game_sku],
                       datetime.now().strftime(config.DATETIME_FORMAT),
                       dicto[config.keyname_game_score]
                       )
                self.cursor.execute(sql, val)
            except Exception:
                pass

