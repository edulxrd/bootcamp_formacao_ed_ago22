import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pandas as pd

Engine = create_engine(
    'postgresql+psycopg2://root:root@localhost/test_db'
)            

#Dar os comandos sql dentro do nosso banco de dados
sql = '''
select *
from vw_artist;
'''

#df = nosso data frame // (nome do comando no caso foi sql ou colocar direto a consulta, nome da engine)
df_artist = pd.read_sql_query(sql,Engine)

df_song = pd.read_sql_query('select * from vw_song',Engine)

#Para executar uma query dentro do banco de dados utilizamos engine.execute(comando, no caso sql)

sql = '''
insert into tb_artist(
SELECT t1."date"
	,t1."rank"
	,t1.artist
	,t1.song 
from public."Billboard" as T1
where T1.artist like 'Drake'
order by t1.artist, t1.song, t1."date"
);
'''

Engine.execute(sql)
