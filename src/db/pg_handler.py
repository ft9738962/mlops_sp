import csv

import psycopg2

from src.utils.config import get_config
from src.utils.directory_utils import find_root

class PgHandler:
    def __init__(self, config):
        self.config = config['postgres_dev']

    def get_connection(self, is_init: bool=False):
        db = 'postgres' if is_init else self.config["database"]
        return psycopg2.connect(
            database=db,
            user=self.config["user"],
            password=self.config["pw"],
            host=self.config["host"],
            port=self.config["port"],
        )

    def initialzie_db(self):
        # 连接到默认的数据库
        conn =self.get_connection(is_init=True)
        conn.autocommit = True  # 开启自动提交模式，以便可以创建新的数据库
        cur = conn.cursor()
        cur.execute("CREATE DATABASE dev;")
        cur.close()
        conn.close()
        print('Create new db: dev')

        with self.get_connection() as conn:
            with conn.cursor() as cur:
                create_train_data_tbl_query = """
                CREATE TABLE train_data (
                    id SERIAL PRIMARY KEY,
                    comment_dt DATE,
                    score SMALLINT,
                    comment TEXT,
                    version INT
                );
                """
                cur.execute(create_train_data_tbl_query)

                cur.execute("CREATE INDEX idx_comment_dt ON train_data(comment_dt);")
                cur.execute("CREATE INDEX idx_version ON train_data(version);")
                cur.execute("CREATE INDEX idx_score ON train_data(score);")

                print("Database and table created successfully!")
            conn.commit()

    def get_latest_version(self) -> int:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT version FROM 
                    train_data ORDER BY version DESC LIMIT 1;
                    ''')
                cur.fetchone()
                return cur.fetchone()[0] if cur.fetchone() else 0
        
    def insert_data(self, data):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                insert_sql = '''
                INSERT INTO train_data (comment_dt, score, comment, version) 
                VALUES (%s, %s, %s, %s);", data);
                '''
                cur.executemany(insert_sql, data)
            conn.commit()

    def read_csv_and_insert(self, file):
        data = []
        ltst_vrsn = self.get_latest_version()
        with open(file, 'r') as file:
            reader = csv.reader(file)
            # 跳过CSV文件的标题行
            next(reader)  
            for row in reader:
                row.append(ltst_vrsn+1)
                data.append(tuple(row))
        print(data)
        # self.insert_data(data)
        print('csv files insert into db')

if __name__ == "__main__":
    csv_path = find_root() / \
        get_config()['file_path']['cleaned_csv']
    pg_handler = PgHandler(get_config())
    pg_handler.read_csv_and_insert(csv_path)

