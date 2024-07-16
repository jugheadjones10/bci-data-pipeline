import os

import dropbox
from dotenv import load_dotenv
from dropbox.exceptions import ApiError, AuthError

load_dotenv()

# Load env var from .env
DROPBOX_ACCESS_TOKEN = os.environ.DROPBOX_ACCESS_TOKEN

# Replace with your local directory path and Dropbox folder path
LOCAL_DIRECTORY = "./Sparky"
DROPBOX_DIRECTORY = "/BMI/Sparky"

# Skip folders that are already there


def download_file(dbx, dropbox_path, local_path):
    try:
        _, response = dbx.files_download(dropbox_path)
        with open(local_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {dropbox_path} to {local_path}")
    except ApiError as e:
        print(f"Error downloading {dropbox_path}: {str(e)}")


def sync_from_dropbox():
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        dbx.users_get_current_account()
    except AuthError:
        print("Invalid access token. Please check your Dropbox access token.")
        return

    try:
        for entry in dbx.files_list_folder(DROPBOX_DIRECTORY, recursive=True).entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                dropbox_path = entry.path_display
                local_path = os.path.join(
                    LOCAL_DIRECTORY, os.path.relpath(dropbox_path, DROPBOX_DIRECTORY)
                )

                # Create local directories if they don't exist
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                # Download the file
                download_file(dbx, dropbox_path, local_path)

    except ApiError as e:
        print(f"Error accessing Dropbox: {str(e)}")


if __name__ == "__main__":
    sync_from_dropbox()
