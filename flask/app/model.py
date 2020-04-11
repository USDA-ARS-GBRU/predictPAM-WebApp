from app.mod_tables.serverside.serverside_table import ServerSideTable
from app.mod_tables.serverside import table_schemas

df = pd.read_csv('out.txt', sep="\t", header=0)
data_dict = df.to_dict()

class TableBuilder(object):

    def collect_data_clientside(self):
        return {'data': data_dict}

    def collect_data_serverside(self, request):
        columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, data_dict, columns).output_result()