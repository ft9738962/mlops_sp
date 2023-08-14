import csv
import psycopg2

from src.utils.config import get_config

class pgHandler:
    def __init__(self, config):
        self.cfg = config['postgres_dev']

    
    def get_connection(self):
        return psycopg2.connect(
            database=self.config["database"],
            user=self.config["user"],
            password=self.config["password"],
            host=self.config["host"],
            port=self.config["port"],
        )

    @use_log
    def initialzie_db(self):
        # 连接到默认的数据库
        with self.get_connection() as conn:
            conn.autocommit = True  # 开启自动提交模式，以便可以创建新的数据库
            cur = conn.cursor()

            # 创建新的数据库dev
            cur.execute("CREATE DATABASE dev;")

            # 连接到新创建的数据库
            conn.close()  # 关闭旧的连接
            conn = psycopg2.connect(database="dev", user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
            cur = conn.cursor()

            create_train_table_query = """
            CREATE TABLE train_data (
                id SERIAL PRIMARY KEY,
                comment_dt DATE,
                score SMALLINT,
                comment TEXT,
                version INT
            );
            """
            cur.execute(create_train_table_query)

            cur.execute("CREATE INDEX idx_comment_dt ON train_data(comment_dt);")
            cur.execute("CREATE INDEX idx_version ON train_data(version);")
            cur.execute("CREATE INDEX idx_score ON train_data(score);")

            print("Database and table created successfully!")

            conn.commit()
            cur.close()

    def get_latest_version(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT version FROM 
                    train_data ORDER BY version DESC LIMIT 1;
                    ''')
                version = cur.fetchone()[0]
        return version
        
    def insert_data(self, data):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                insert_sql = '''
                INSERT INTO train_data (comment_dt, score, comment, version) 
                VALUES (%s, %s, %s, %s);", data);
                '''
                cur.executemany(insert_sql, data)
                conn.commit()

if __name__ == "__main__":
    config = get_config()
    pg_handler = pgHandler(config)
    pg_handler.initialzie_db()

