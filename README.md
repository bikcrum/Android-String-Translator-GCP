## Find iOS string translator here https://github.com/bikcrum/iOS-String-Translator-GCP

# Translator for Android string resource

### How to bulk translate?

#### Prerequisites

1. Must have python version 3
2. Must have billing enabled in Google Cloud Platform (GCP)
2. Install this python package (if not installed).
    1. bs4
3. Install the google client translation library `pip install --upgrade google-cloud-translate`

#### Steps:

1. Goto GCP console (https://console.cloud.google.com/) then under IAM & Admin click Service accounts. 
2. Create service account and assign a role as project owner.
3. Create key which will be downloaded into your computer.
4. Clone and go to the project directory
5. Put service account there and rename to `project-service-account.json`
6. Use this command ``python translator-for-android.py <source-string-file> <languages list>``
7. Example ``python translator-for-android.py strings.xml fr`` or  ``python translator-for-android.py strings.xml fr,de,nl``
8. To translate to all available languages just provide source string in the command
9. After above operation you will get new translated file(s) in current directory
