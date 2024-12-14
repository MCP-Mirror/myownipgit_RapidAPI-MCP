# Patent Scoring System

This document describes the scoring methodology used in the RapidAPI MCP system.

## Overview

The scoring system consists of four main components:

1. Patent Score (pscore)
2. Citation Score (cscore)
3. Legal Score (lscore)
4. Technology Score (tscore)

## Scoring Components

### Patent Score (pscore)

The patent score is a composite score that considers multiple factors:

- Number of claims (20%)
- Citation count (30%)
- Patent family size (20%)
- Patent age (15%)
- Legal status (15%)

Formula:
```
pscore = (w_claims * claims_score + w_citations * citations_score + 
          w_family * family_score + w_age * age_score + 
          w_legal * legal_score) * 100
```

### Citation Score (cscore)

The citation score focuses on the impact of the patent through its citations:

- Forward citations (weighted 1.5x)
- Backward citations (weighted 1.0x)

### Legal Score (lscore)

The legal score evaluates the legal strength and status:

- Active status (+25 points)
- No oppositions filed (+15 points)
- Granted status (+10 points)
- Base score (50 points)

### Technology Score (tscore)

The technology score assesses technical complexity:

- Number of CPC codes (>3 codes: +15 points)
- Claim complexity (>20 claims: +10 points)
- Technical illustrations (>5 figures: +10 points)
- Base score (50 points)

## Score Normalization

All scores are normalized to a 0-100 scale where:
- 0-20: Very Low
- 21-40: Low
- 41-60: Medium
- 61-80: High
- 81-100: Very High