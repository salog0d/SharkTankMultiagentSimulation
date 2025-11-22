JUDGE_EVALUATION_PROMPT = """You are an investor evaluating a startup pitch.

Judge profile:
{judge}

Pitch:
{entrepreneur}

Narrate your evaluation:
- What impressed you
- What concerns you
- How it fits your investment thesis
- Your view on risk and upside
"""

JUDGE_OFFER_PROMPT = """You are an investor explaining your offer.

Judge:
{judge}

Offer:
{offer}

Explain:
- Why you chose this amount and equity
- How you see risk vs reward
- What conditions you implicitly assume
"""
