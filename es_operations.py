from utils import *
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['localhost:9200'],
    # sniff before doing anything
    sniff_on_start=True,
    # refresh nodes after a node fails to respond
    sniff_on_connection_fail=True,
    # and also every 60 seconds
    sniffer_timeout=60
)

if __name__ == "__main__":
    pass







