# SocialBoost AI

Responsive FastAPI starter website with:
- Instagram, Facebook and YouTube creator dashboard placeholders
- AI content ideas and caption/hashtag helper endpoints
- Monetization checklist
- Subscription pricing presentation (Free / Pro / Business)
- Creator services showcase
- Advertising placement placeholder

## Run locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
Open http://127.0.0.1:8000

## Deploy
Create a new GitHub repository and deploy as a Render Web Service using the included Dockerfile.

## Important setup still required
This is a front-end/business-model starter, not a live payment or analytics platform yet.
Before taking real payments, have a parent/guardian or eligible adult account holder review and set up the business, payment provider, refunds, taxes, privacy policy and terms. Add a supported payment provider and server-side webhook verification.
Live Instagram/Facebook/YouTube analytics require official OAuth/API access and platform approvals.
Advertising requires an approved ad network account and compliant site/content.
Do not implement fake followers, likes, views, comments, bots, or credential collection.
