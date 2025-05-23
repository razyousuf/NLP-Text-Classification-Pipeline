#from hate.logger import logging
#logging.info("This is a test log message.")

##########################################
# from hate.exception import CustomException
# import sys

# try:
#     a = 1 / 0
# except Exception as e:
#     raise CustomException(e, sys) from e

######################################

from hate.configuration.gcloud_syncer import GCloudSync

obj = GCloudSync()
obj.sync_folder_from_gcloud("hate-speach-2025", "dataset.zip", "download/dataset.zip")

