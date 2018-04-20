from abv.inventory_api.filter_ds import FilterDS
from abv.inventory_api.inventory_queries import InventoryQueries


class TwilioInterface:

    def __init__(self, msg):
        self.msg = msg

    def extract_info_and_query(self):
        parse_msg = self.msg.split(" ")
        filtered_msg = FilterDS(size=parse_msg[1], name=parse_msg[0])
        return InventoryQueries.get_filtered_inventory(filtered_msg)
        






#extract msssage, turn to filter ds then send it to get_filtered_inventory