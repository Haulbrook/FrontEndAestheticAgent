"""
AI Prompt Templates for Disney Trip Planner
Centralized prompt engineering for easy iteration and testing
"""

# ============================================================================
# SYSTEM PROMPT - Core AI Personality
# ============================================================================
SYSTEM_PROMPT = """You are an expert Disney trip planning assistant with deep knowledge of:
- Walt Disney World, Disneyland, and other Disney destinations
- Trip planning logistics and timelines
- Family travel needs and considerations
- Disney-specific tips, tricks, and hidden gems

Your role is to help families plan magical Disney vacations by:
1. Creating comprehensive, personalized checklists
2. Brainstorming creative ideas and suggestions
3. Anticipating needs (both obvious and easily forgotten)
4. Providing actionable, specific advice
5. PROACTIVELY suggesting checklist items when appropriate

IMPORTANT CHECKLIST MANAGEMENT:
- When you identify something the traveler should remember to pack or prepare, you can suggest adding it to their checklist
- Use this special format ANYWHERE in your response: [ADD_ITEM: item_description | category | priority]
  - item_description: Clear, actionable description (e.g., "Pack portable phone charger")
  - category: shopping, packing, health, tech, home-prep, or travel-day
  - priority: high, medium, or low
- You can suggest multiple items in one response
- Examples:
  * "That's a great idea! [ADD_ITEM: Pack cooling towels for hot days | packing | medium]"
  * "Don't forget [ADD_ITEM: Download My Disney Experience app | tech | high] before you go!"
  * "Based on your party having young kids, [ADD_ITEM: Bring stroller or carrier | packing | high] would be helpful."

When user explicitly asks you to "add to checklist" or "remind me", definitely suggest the item.
When you notice they might need something based on context, proactively suggest it.

Be enthusiastic, helpful, and thorough. Consider different age groups, special needs,
budget constraints, and timeframes when making recommendations."""

# ============================================================================
# CHECKLIST GENERATION PROMPT
# ============================================================================
CHECKLIST_PROMPT_TEMPLATE = """Generate a comprehensive Disney trip PERSONAL PREPARATION checklist for the following trip:

Destination: {destination}
Trip Date: {start_date}
Days Until Trip: {days_until}
Party Size: {party_size}
Ages: {ages}
Interests: {interests}
Budget: {budget_range}
Special Needs: {special_needs}

CRITICAL REQUIREMENTS:
1. Focus ONLY on personal preparation items (what to pack, what to do before leaving)
2. DO NOT include Disney park planning activities (like "book restaurants" or "plan itinerary")
3. Include 20-30 items that are:
   - Actionable and specific
   - Appropriate for the party composition (ages, interests)
   - Include both obvious and easily-forgotten items
   - Prioritized (high/medium/low)
4. Consider the {trip_phase} phase ({days_until} days away):
   - Early: focus on big purchases, preparations
   - Mid: focus on gathering items, booking
   - Final: focus on packing, last-minute tasks
   - Imminent: focus on essential last-minute checks

CATEGORIES TO USE:
- shopping: Items to buy/purchase before trip
- packing: Items to pack in luggage
- health: Medical, fitness, health preparations
- tech: Apps, devices, charging equipment
- home-prep: Preparing house for absence
- travel-day: Day-of-travel essentials

Return ONLY a JSON object with this structure:
{{
  "items": [
    {{
      "text": "Item description",
      "category": "category_name",
      "priority": "high|medium|low",
      "deadline": "Optional deadline info"
    }}
  ]
}}

DO NOT include explanatory text outside the JSON."""

# ============================================================================
# BRAINSTORMING PROMPT
# ============================================================================
BRAINSTORMING_PROMPT_TEMPLATE = """Generate creative Disney trip ideas for:

Destination: {destination}
Trip Date: {start_date}
Party Size: {party_size}
Ages: {ages}
Interests: {interests}
Budget: {budget_range}

Generate 15-20 specific, actionable ideas across these categories:
1. Dining experiences (restaurants, snacks, unique food items)
2. Activities & attractions (rides, shows, experiences)
3. Photo opportunities (specific locations, poses, magical moments)
4. Surprises & special touches (ways to make the trip extra magical)
5. Insider tips (time-savers, money-savers, hidden gems)

Make ideas:
- Specific to Disney parks and resorts
- Appropriate for the party's age range
- Aligned with stated interests
- Varied in cost (some free, some budget-friendly, some splurge-worthy)
- Actionable with clear next steps

Return ONLY a JSON object with this structure:
{{
  "ideas": [
    {{
      "title": "Short, catchy title",
      "description": "2-3 sentence description with actionable details",
      "category": "dining|activities|photos|surprises|tips",
      "tags": ["tag1", "tag2"]
    }}
  ]
}}

DO NOT include explanatory text outside the JSON."""

# ============================================================================
# FORGOTTEN ITEMS PROMPT
# ============================================================================
FORGOTTEN_ITEMS_PROMPT_TEMPLATE = """Based on this Disney trip checklist, identify items that are COMMONLY FORGOTTEN:

Current Checklist:
{current_checklist}

Trip Details:
- Destination: {destination}
- Party Size: {party_size}
- Ages: {ages}
- Special Needs: {special_needs}

Analyze what's missing and suggest 5-10 items that travelers commonly forget, such as:
- Phone chargers/portable batteries
- Medication/first aid items
- Weather-appropriate gear
- Comfort items for kids
- Travel documents/copies
- Snacks for picky eaters
- Entertainment for travel time
- Specific items for special needs

Return ONLY a JSON object with this structure:
{{
  "suggestions": [
    {{
      "text": "Item description",
      "category": "category_name",
      "priority": "high|medium|low",
      "reason": "Why this is commonly forgotten"
    }}
  ]
}}

DO NOT include explanatory text outside the JSON."""

# ============================================================================
# PERSONALIZED SUGGESTION PROMPT
# ============================================================================
PERSONALIZED_SUGGESTION_PROMPT_TEMPLATE = """Answer this Disney trip planning question:

User Question: {question}

Trip Context:
- Destination: {destination}
- Trip Date: {start_date}
- Days Until: {days_until}
- Party: {party_size} people, ages {ages}
- Interests: {interests}
- Budget: {budget_range}

Provide a helpful, specific answer that:
1. Directly addresses their question
2. Considers their specific trip context
3. Includes actionable advice
4. Suggests relevant checklist items using [ADD_ITEM: text | category | priority]
5. Is enthusiastic and encouraging

Keep response 2-4 paragraphs. Be conversational and friendly."""

# ============================================================================
# FALLBACK CHECKLIST (if API fails)
# ============================================================================
FALLBACK_CHECKLIST = [
    {"text": "Valid ID and tickets", "category": "Documents", "priority": "high"},
    {"text": "Phone charger and portable battery", "category": "Electronics", "priority": "high"},
    {"text": "Comfortable walking shoes", "category": "Clothing", "priority": "high"},
    {"text": "Sunscreen and sunglasses", "category": "Park Essentials", "priority": "high"},
    {"text": "Refillable water bottle", "category": "Park Essentials", "priority": "medium"},
    {"text": "Light rain jacket or poncho", "category": "Clothing", "priority": "medium"},
    {"text": "Basic first aid supplies", "category": "Toiletries", "priority": "medium"},
    {"text": "Snacks for picky eaters", "category": "Comfort Items", "priority": "medium"},
    {"text": "Autograph book and pen", "category": "Special Items", "priority": "low"},
    {"text": "Camera or phone with good storage", "category": "Electronics", "priority": "low"},
]
