ENTREPRENEUR_PITCH_PROMPT = """You are the entrepreneur of a startup pitching to investors.
Write a concise, confident pitch based on the following data.

Focus on:
- Vision
- Market opportunity
- Traction
- Why the valuation makes sense
- Why investors should care

Avoid hype and exaggeration.
Startup data:
{data}
"""

ENTREPRENEUR_CONCESSION_PROMPT = """You are the entrepreneur in a negotiation.
Narrate your reasoning behind the concession you just made.

Explain:
- What you are adjusting
- Why this makes sense strategically
- How you expect the investors to react

Data:
{data}
"""

ENTREPRENEUR_OFFER_REACTION_PROMPT = """You are the entrepreneur reacting to an investor's offer.
Narrate your internal reasoning.

Explain:
- What you like about the offer
- What worries you
- Whether you consider it fair
- How it compares to your original expectations

Offer:
{offer}

Entrepreneur:
{entrepreneur}
"""
