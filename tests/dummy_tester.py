from dbtalker_psql import DBTalker

stupid = "HRKU-4e9e0d78-2234-4999-8391-13e14ec05360"

dummy = DBTalker(api_key=stupid)

sqlCommand = """"""
para = ()

results = dummy.callToDB(sqlCommand=sqlCommand, para=para)

print(results)