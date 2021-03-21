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

    def __connect_to_db(self, config_file):
        """Returns mysql connector object. In order to create the connection,
            the method contains very sensitive data.
        """
        if config_file.mysql_native_authentication:
            return mysql.connector.connect(
                host=config_file.MYSQL_HOST,
                user=config_file.mysql_user,
                password=config_file.mysql_password,
                database=config_file.MYSQL_DATABASE,
                auth_plugin=config_file.MYSQL_AUTH
            )
        else:
            return mysql.connector.connect(
                host=config_file.MYSQL_HOST,
                user=config_file.mysql_user,
                password=config_file.mysql_password,
                database=config_file.MYSQL_DATABASE
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
                val = (dicto[config.KEYNAME_GAME_SKU],
                       dicto[config.KEYNAME_GAME_TITLE],
                       dicto[config.KEYNAME_RELEASE_DATE],
                       dicto[config.KEYNAME_WORKS_ON],
                       ', '.join(set(dicto[config.KEYNAME_COMPANY])),
                       dicto[config.KEYNAME_GAME_SIZE],
                       dicto[config.KEYNAME_GAME_URL])
                self.cursor.execute(sql, val)
            except Exception:
                pass

    def write_game_genres(self):
        """Write into game_genres the genres of the game.
        Each game could have at 3 different types of genres => each one in a row
        """
        for dicto in self._data:  # todo: change dicto name
            for genere_name in dicto[config.KEYNAME_GENRE]:
                try:
                    sql = """INSERT INTO game_genres (title_sku, genre_name) VALUES(%s,%s) 
                             ON DUPLICATE KEY UPDATE 
                                genre_name = VALUES(genre_name)             
                            """
                    val = (
                        dicto[config.KEYNAME_GAME_SKU], genere_name)
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
                val = (dicto[config.KEYNAME_GAME_SKU],
                       datetime.now().strftime(config.DATETIME_FORMAT),
                       dicto[config.KEYNAME_GAME_BASE_PRICE],
                       dicto[config.KEYNAME_GMAE_FINAL_PRICE],
                       dicto[config.KEYNAME_GAME_DISCOUNT]
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
                val = (dicto[config.KEYNAME_GAME_SKU],
                       datetime.now().strftime(config.DATETIME_FORMAT),
                       dicto[config.KEYNAME_GAME_SCORE]
                       )
                self.cursor.execute(sql, val)
            except Exception:
                pass

