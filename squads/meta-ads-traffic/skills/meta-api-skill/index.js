const bizSdk = require('facebook-nodejs-business-sdk');
require('dotenv').config();

const AdAccount = bizSdk.AdAccount;
const Campaign = bizSdk.Campaign;
const AdSet = bizSdk.AdSet;
const Ad = bizSdk.Ad;

const access_token = process.env.META_ACCESS_TOKEN;
const app_secret = process.env.META_APP_SECRET;
const app_id = process.env.META_APP_ID;
const ad_account_id = process.env.META_AD_ACCOUNT_ID;

const api = bizSdk.FacebookAdsApi.init(access_token);
const account = new AdAccount(ad_account_id);
// const account = new AdAccount('act_' + ad_account_id); // Ensure 'act_' prefix if not present in env

async function listCampaigns() {
    try {
        const campaigns = await account.getCampaigns(
            [Campaign.Fields.name, Campaign.Fields.status, Campaign.Fields.objective],
            { limit: 10 }
        );
        return campaigns.map((c) => ({
            id: c.id,
            name: c.name,
            status: c.status,
            objective: c.objective,
        }));
    } catch (error) {
        console.error('Error fetching campaigns:', error);
        throw error;
    }
}

async function getAccountInsights() {
    try {
        const insights = await account.getInsights(
            ['spend', 'impressions', 'clicks', 'cpc', 'cpm', 'ctr'],
            { date_preset: 'last_7d' }
        );
        return insights;
    } catch (error) {
        console.error('Error fetching insights:', error);
        throw error;
    }
}

async function run() {
    const command = process.argv[2];

    if (command === 'list-campaigns') {
        const campaigns = await listCampaigns();
        console.log(JSON.stringify(campaigns, null, 2));
    } else if (command === 'account-insights') {
        const insights = await getAccountInsights();
        console.log(JSON.stringify(insights, null, 2));
    } else {
        console.log('Usage: node index.js <command>');
        console.log('Commands: list-campaigns, account-insights');
    }
}

run();
