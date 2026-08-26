# What I checked, and what the agent got wrong

## What the agent got wrong

The agent initially changed the constants and the warning threshold, which was incorrect because the rules defined in `config_loader` should not be touched. Instead of fixing the actual underlying problem, it initially tried to change the setup so that the tests would pass. That was not a proper long-term solution because it changed existing rules rather than fixing the wear calculation.

## What I checked before I accepted its work

After giving clearer prompts and explicitly saying "DON'T CHANGE KNOWN_KEYS", the agent fixed the actual problem correctly. I ran `pytest` myself and confirmed that all 4 tests passed. I also checked the wear calculation directly and confirmed that it returned the correct value instead of 0. This showed that the `//` floor division bug had been fixed by changing it to `/`. To make sure the 80% rule was untouched, I checked the diff and confirmed that `WARN_AT_PERCENT = 80` had no `+` or `-` change.

## What the data actually said

The data showed that `km_since_service`, `avg_daily_km`, and `load_factor` were the strongest factors associated with breakdowns. The obvious-looking factors, `odometer_km` and `age_years`, were not as effective and were not useful indicators compared with the three stronger factors above.
