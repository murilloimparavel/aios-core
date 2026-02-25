# Meta API Skill

This skill provides direct integration with the Meta Marketing API using `facebook-nodejs-business-sdk`.

## Dependencies
- Node.js
- `facebook-nodejs-business-sdk`
- `dotenv`

## Setup
Ensure the following environment variables are set in your `.env` file:
```env
META_ACCESS_TOKEN=...
META_APP_SECRET=...
META_APP_ID=...
META_AD_ACCOUNT_ID=act_...
```

## Usage
Run the script with the desired command:
```bash
node squads/meta-ads-traffic/skills/meta-api-skill/index.js list-campaigns
node squads/meta-ads-traffic/skills/meta-api-skill/index.js account-insights
```

## Supported Commands
- `list-campaigns`: Fetches the last 10 campaigns with status and objective.
- `account-insights`: Fetches account-level insights for the last 7 days (Spend, CPM, CPC, CTR).
