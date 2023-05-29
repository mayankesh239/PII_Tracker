# PII_Tracker App

This application is designed to periodically fetch data from a public GitHub repository file like [this](https://github.com/mayankesh239/GDSC-website/blob/master/general.json) containing patterns for Personally Identifiable Information (PII) data which the help of __github acess token__. It then synchronizes the data with a MongoDB collection.

- It fetches data periodically from the GitHub file specified by the link.
- It stores the fetched data in a MongoDB collection.
- It handles additions, updates, and deletes of entries in the GitHub file, reflecting the changes in the MongoDB collection on the next run.
- The code is written in Python.
- It handles edge cases such as handling GitHub API errors, checking for the last synchronized commit, comparing commits to determine if there are new changes, and logging errors for debugging purposes.


Note: it only collects the useful informations ( entries for which `sensitive is marked as true` in the file).

## Milestones achieved

1. Given a GitHub link to a file like [this](https://github.com/mayankesh239/GDSC-website/blob/master/general.json) which contains patterns for PII data, a cron mentioned [here](https://github.com/mayankesh239/GDSC-website/blob/master/general.json) will periodically run and fetch data from this file and store this in a mongo collection.

2. Note that if a new entry is added to the file, then the same would be reflected in mongo on the next run. Same goes for updates and deletes as well.

## Requirements

- Python 3.x
- pip (Python package installer)
- GitHub access token
- MongoDB URI

## Installation

1. Clone the repository:
  ```
  $ git clone https://github.com/your-username/pii-sync-app.git
  ```

2. Navigate to the project directory:
  ```
  $ cd pii-sync-app
  ```

3. Install the required Python packages:
  ```
  $ pip install -r requirements.txt
  ```

## Configuration

1. Generate a GitHub access token:
- Go to https://github.com/settings/tokens.
- Click on "Generate new token".
- Give the token a suitable description and select the necessary scopes (e.g., repo access).
- Click on "Generate token" and copy the generated access token.

2. Set the MongoDB URI:
- Open `main.py` file in a text editor.
- Replace the value of `mongodb_uri` variable (at line no 18 ) with your MongoDB connection URI.
 You can refer this [Create Cluster Using MongoDB Atlas](https://docs.google.com/document/d/1CviQ3No4yMwsjREFgg24yV1wBf2knBMoHgV8EOj17kE/edit?usp=sharing)) to create cluster in MongoDB Atlas.
  
3. Configure the application:
- Open the main.py file.
- Update the following variables in the code:
    * repository_url: Set it to the GitHub repository URL containing the PII data file.
    * file_path: Set it to the file path of the PII data file within the repository.
    * mongodb_uri: Set it to the connection URI for your MongoDB database.
    * database_name: Set it to the name of the MongoDB database.
    * collection_name: Set it to the name of the MongoDB collection.
    * GITHUB_ACCESS_TOKEN: Set it to your GitHub access token.

## Usage

To run the application and perform data synchronization, execute the following command in the project directory:

  ```
  $ python3 main.py
  ```

The application will fetch data from the this GitHub repository [file](https://github.com/mayankesh239/GDSC-website/blob/master/general.json), filter the sensitive information based on the "sensitive" attribute, and update the MongoDB collection with the filtered data. It will log the execution status and any errors encountered in the `pii_sync.log` file.

## Cron Job Configuration

To set up a cron job for periodic execution, you can use the `crontab` command on Linux systems:

1. Open the terminal and execute the following command:
  ```
  $ crontab -e
  ```
  If prompted to select an editor, choose your preferred editor (e.g., nano, vim).
  
2. Add the following line to the crontab file to schedule the job at 8:30 PM every day:
  ```
  30 20 * * * /usr/bin/python3 /path/to/your/pii-sync-app/main.py 
  ```
Replace `/path/to/your/pii-sync-app` with the actual path to the project directory. Save the crontab file and exit the editor.

3. Execute the following command:
  ```
  sudo apt install postfix
  ```
During the installation, you will be prompted to choose the general type of configuration. Select "Internet Site" and press Enter. Then, enter your fully qualified domain name (FQDN) when prompted. If you don't have a registered domain name, you can use the hostname of your server as the FQDN. To find out the hostname, you can run the following command in your terminal:

  ```
  hostname
  ```

4. Save the file and exit the text editor.

The cron job will now run at the specified time and execute the PII synchronization process.  You can check the execution and any potential error messages in the log file specified in your script's logging configuration (pii_sync.log in this case).

You can check the scheduled cron jobs by running the following command in the terminal:
  ```
  crontab -l
  ```

If the cron job is not working you can refer [this](https://docs.google.com/document/d/1_BUI6k9hF7IWwPvSHw9Kq0CMRf0g5QMpY1luzwC6iV4/edit). This doc has a list some of the ways to fix the issues.

Note: this will work in linux. You can use task scheduler to perform this on windows ( [refer this](https://docs.google.com/document/d/1pPUWmuMvIDrEsyn7dUwCYvBZW6IP2PPn3iKtRDLvExw/edit?usp=sharing) ) 
