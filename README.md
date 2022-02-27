Buy some VPS to run script 24 hours per day, then follow steps below

1. `pip install -r requirements.txt`

2. create .env file 
    - `touch .env`

3. paste to the .env file yours wallet address and private key for this address
    - `ADDRESS=0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
    - `KEY=0xVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV`

4. use crontab to run script automatically
   - `crontab -e`
   - `*/2 * * * * python3 /PATH_TO_FILE/run.py`

5. Configure:
   - HOW_MANY_PLANTS = 1 # if 1 compound each plant, e.g 5 - wait for 5 plant to compound
   - MAX_PLANTS = 2000   # compound to this value and stop
   - MIN_BALANCE = 0.01  # minimum account BNB balance below which stop compound

If this is helpful, send me an airdrop for beer:
 0x74ABf1db8c8b45aD529Bd3012bE1990F605360D6