from upload_to_mongodb import process_dataset, persist_data, print_summary, export_data
from upload_to_es import ESUploader
import time


def upload_data_to_mongodb():
    data = process_dataset("./dataset/players-data.json")
    persist_data(data)
    export_data("./dataset/mongo-players-data.json")
    print_summary(data)


def upload_data_to_elasticsearch():
    uploader = ESUploader()
    players_data = uploader.load_data("./dataset/mongo-players-data.json")
    if players_data:
        if uploader.upload_players(players_data):
            uploader.verify_upload()


if __name__ == "__main__":
    upload_data_to_mongodb()
    time.sleep(30)
    upload_data_to_elasticsearch()
