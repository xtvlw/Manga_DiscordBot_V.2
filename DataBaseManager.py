from sqlite3 import connect
from os import getcwd

client = connect(f'{getcwd()}/Documents/python/MangaBotV2/database.db')
cursor = client.cursor()

def maneger(table, id, manga_name='', Value=False):
    if Value == True:
        try:
            names = cursor.execute(f"SELECT * FROM {table}_{id}")
            for name in names:
                manga_name += f'-{name[0]}\n'
            return manga_name
        except:
            return 'Vazio'
    else:
        if 'capitulo' in manga_name:
            manga_name = manga_name[:manga_name.find(' capitulo')]
        table = f'{table}_{id}'
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} (manga_name text)')
        client.commit()
        rows = cursor.execute(f'SELECT * FROM {table}')
        names = []
        for row in rows:
            names += [row[0]]
        if manga_name in names:
            cursor.execute(f"DELETE FROM {table} WHERE manga_name='{name}'")
        else:
            if 'readed' in table:
                try:
                    cursor.execute(f"DELETE FROM read_later_{id} WHERE manga_name='{manga_name}'")
                except:
                    pass
            cursor.execute(f"INSERT INTO {table} VALUES ('{manga_name}')")
    client.commit()
