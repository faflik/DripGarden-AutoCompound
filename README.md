Buy some VPS to run script 24 hours per day, then follow steps below

1. `pip install -r requirements.txt`

2. create .env file 
    `touch .env`

3. paste to the .env file yours wallet address and private key for this address
    ADDRESS=0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    KEY=0xVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

4. use crontab to run script automatically
    `crontab -e`
    `*/2 * * * * python3 /PATH_TO_FILE/run.py`
