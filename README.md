

Buy some VPS or Raspberry PI to run script 24 hours per day, then follow steps below

1. `pip install -r requirements.txt`

2. create .env file 
    - `touch .env`

3. paste to the .env file yours wallet address and private key for this address
    - `ADDRESS=0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
    - `KEY=0xVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV`

    If you have hardware wallet use "mnemonic code converter"

4. use crontab to run script automatically every two minutes
   - `crontab -e`
   - `*/2 * * * * python3 /PATH_TO_FILE/run.py`

5. To configure edit config.py:
   - HOW_MANY_PLANTS = 10   # if 1 compound each plant, e.g 10 - wait for 10 plant to compound
   - MIN_BALANCE = 0.02     # minimum account BNB balance below which stop compound
   - LP_DAY = 3.500         # Limit Lp per Day. Below plant seeds, above sell seeds

   - PERIOD = 0             # 0 - plant every HOW_MANY_PLANTS
                            # 1 - harvest every HOW_MANY_PLANTS
                            # e.g. 3 - harvest every third HOW_MANY_PLANTS, first and second plant

If this is helpful, send me an airdrop for beer:
 0x74ABf1db8c8b45aD529Bd3012bE1990F605360D6