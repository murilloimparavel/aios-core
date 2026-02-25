/**
 * Meta Ads API Client
 * 
 * Abstracted functions for programmatic media buying, campaign configuration,
 * and insight analysis for the meta-ads-traffic squad.
 */

const axios = require('axios');

class MetaApiClient {
    constructor(accessToken, adAccountId, version = 'v20.0') {
        this.accessToken = accessToken;
        this.adAccountId = adAccountId; // e.g., '1234567890' (without act_ prefix)
        this.baseUrl = `https://graph.facebook.com/${version}`;
        this.accountPath = `/act_${this.adAccountId}`;
    }

    /**
     * Helper to make API requests with error handling
     */
    async _request(method, endpoint, data = null, params = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method,
            url,
            params: { access_token: this.accessToken, ...params },
            data
        };

        try {
            const response = await axios(config);
            return response.data;
        } catch (error) {
            console.error(`Meta API Error (${method} ${endpoint}):`, error.response?.data || error.message);
            throw new Error(`Meta API Error: ${JSON.stringify(error.response?.data?.error || error.message)}`);
        }
    }

    // ==========================================
    // CAMPAIGN CREATION & CONFIGURATION
    // ==========================================

    /**
     * Creates a new Campaign
     * @param {string} name - Campaign name
     * @param {string} objective - e.g., 'OUTCOME_TRAFFIC', 'OUTCOME_SALES'
     * @param {string} status - 'ACTIVE', 'PAUSED'
     */
    async createCampaign(name, objective, status = 'PAUSED') {
        const data = {
            name,
            objective,
            status,
            special_ad_categories: ['NONE']
        };
        return this._request('POST', `${this.accountPath}/campaigns`, data);
    }

    /**
     * Creates an Ad Set (Configures Traffic routing, budget, and targeting)
     * @param {string} campaignId 
     * @param {string} name 
     * @param {number} dailyBudget - In cents (e.g., 1000 = $10.00)
     * @param {string} optimizationGoal - e.g., 'LINK_CLICKS', 'IMPRESSIONS'
     * @param {string} billingEvent - e.g., 'IMPRESSIONS'
     * @param {number} bidAmount - Bid cap in cents
     * @param {object} targeting - JSON object for audience targeting
     */
    async createAdSet(campaignId, name, dailyBudget, optimizationGoal, billingEvent, bidAmount, targeting) {
        const data = {
            campaign_id: campaignId,
            name,
            daily_budget: dailyBudget,
            optimization_goal: optimizationGoal,
            billing_event: billingEvent,
            bid_amount: bidAmount,
            targeting: JSON.stringify(targeting),
            status: 'PAUSED'
        };
        return this._request('POST', `${this.accountPath}/adsets`, data);
    }

    // ==========================================
    // ADS & CREATIVES
    // ==========================================

    /**
     * Creates an Ad Creative
     * @param {string} pageId - Facebook Page ID
     * @param {string} imageHash - Hash of the uploaded image
     * @param {string} message - Primary text
     * @param {string} link - Destination URL
     */
    async createAdCreative(name, pageId, imageHash, message, link) {
        const objectStorySpec = {
            page_id: pageId,
            link_data: {
                image_hash: imageHash,
                link: link,
                message: message
            }
        };
        const data = {
            name,
            object_story_spec: JSON.stringify(objectStorySpec)
        };
        return this._request('POST', `${this.accountPath}/adcreatives`, data);
    }

    /**
     * Creates the actual Ad linking Ad Set and Creative
     */
    async createAd(name, adSetId, creativeId, status = 'PAUSED') {
        const data = {
            name,
            adset_id: adSetId,
            creative_id: creativeId,
            status
        };
        return this._request('POST', `${this.accountPath}/ads`, data);
    }

    // ==========================================
    // METRICS & ANALYSIS (PPC AUDIT)
    // ==========================================

    /**
     * Fetches Insights for a specific Campaign
     * @param {string} campaignId 
     * @param {string} datePreset - e.g., 'last_30d', 'maximum'
     */
    async getCampaignInsights(campaignId, datePreset = 'last_30d') {
        const params = {
            level: 'campaign',
            fields: 'impressions,clicks,spend,cpc,ctr,actions,cost_per_action_type',
            date_preset: datePreset
        };
        return this._request('GET', `/${campaignId}/insights`, null, params);
    }

    /**
     * Runs a basic PPC Health Audit to calculate an Ads Health Score
     * Mock implementation inspired by Claude Code PPC skills
     */
    async runPpcHealthAudit() {
        console.log(`[PPC Audit] Starting health check for account ${this.adAccountId}...`);

        // 1. Fetch all active campaigns
        const campaigns = await this._request('GET', `${this.accountPath}/campaigns`, null, { fields: 'name,status', effective_status: "['ACTIVE']" });

        if (!campaigns.data || campaigns.data.length === 0) {
            return { score: 0, recommendations: ['No active campaigns found. Start by launching a new campaign.'] };
        }

        let totalScore = 100;
        const recommendations = [];

        // Analyze each campaign's insights
        for (const campaign of campaigns.data) {
            const insights = await this.getCampaignInsights(campaign.id, 'last_7d');
            const data = insights.data && insights.data[0] ? insights.data[0] : null;

            if (!data) {
                totalScore -= 10;
                recommendations.push(`Campaign '${campaign.name}' has no delivery in the last 7 days. Check targeting and budget.`);
                continue;
            }

            const ctr = parseFloat(data.ctr || 0);
            if (ctr < 1.0) {
                totalScore -= 5;
                recommendations.push(`Campaign '${campaign.name}' has a low CTR (${ctr}%). Consider refreshing Ad Creatives or A/B testing copy.`);
            }
        }

        return {
            accountId: this.adAccountId,
            healthScore: Math.max(0, totalScore),
            activeCampaigns: campaigns.data.length,
            recommendations
        };
    }
}

module.exports = MetaApiClient;
