import pandas as pd
from dataclasses import dataclass
from database.Connectors import *

@dataclass
class VendorList:
    connector: any

    def define_vendorlist(self, query):
        if not self.connector.connection:
            raise Exception("No active connection. Call 'connect()' first.")

        with self.connector.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            vendor = pd.DataFrame(result, columns = columns)

        return vendor
    

    

