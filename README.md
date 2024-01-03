### File Synchronization Service

This program allows synchronize files in your local directory with remote Yandex Disk.

## Getting Started

To begin with, you should get OAuth token. You may do this by running a method.

### Prerequisites

Get token.

```
cloud_connector.get_oauth_token()
```

## Installing

Insert certain data to config.ini. I have provide example: "config.ini.template".

1. Create a file - config.ini

```
config.ini
```

2. Copy data from "config.ini.template".

```
config.ini.template
```

3. From (https://oauth.yandex.ru/) get ClientID and Client secret.

4. Paste them in your config.ini file.

5. Also add a name of local directory and come up with cloud directory(cloud directory will be created automatically)

## Main actions:

1. Endless while loop is located in function - # create_folder
If cloud directory is absent it will be created in Yandex Disk.

2. It is being checking whole local directory and files are being comparing with period of synchronization. The time delta is: current time - the date of modification.

```
                delta_time = (date_time_utc - modified_local_file).seconds
                if int(connection.frequency_sync_period) > delta_time / 60
```
# Pay attention that we indicated time in minutes. In config.ini we insert just minutes for instance 1, 25, 30, 45 and etc.

3. If any file is detected then it's being reloading on remote directory.

4. If it isn't any changes that there are 2 variants:

    1. The file is new created so it hasn't been detected.
    2. The file is deleted from the local directory so it should be deleted from cloud.

5. Then we wait for difinite time.
