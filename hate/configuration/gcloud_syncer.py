import os


class GCloudSync: # Syncing files to and from Google Cloud Storage
    def sync_folder_to_gcloud(self, gcp_bucket_url, filepath, filename):
        """
        Syncs a folder to a Google Cloud Storage bucket.

        :param gcp_bucket_url: str, the URL of the GCP bucket
        :param filepath: str, the path to the folder to be synced
        :param filename: str, the name of the file to be synced
        :destination: str, the destination file in the GCP bucket
        """
        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        os.system(command)
    def sync_folder_from_gcloud(self, gcp_bucket_url, filename, destination):
        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        os.system(command)