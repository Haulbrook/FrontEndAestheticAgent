"""
Disney Trip Planning Agent - AI-powered trip planning assistant
"""
import os
import json
import re
from typing import List, Dict, Any, Tuple
from openai import OpenAI
from datetime import datetime
import pytz

from src.models.trip_data import TripDetails, ChecklistItem, IdeaSuggestion
from src.utils.helpers import get_trip_phase, generate_checklist_id
from src.config.prompts import (
    SYSTEM_PROMPT,
    CHECKLIST_PROMPT_TEMPLATE,
    BRAINSTORMING_PROMPT_TEMPLATE,
    FORGOTTEN_ITEMS_PROMPT_TEMPLATE,
    PERSONALIZED_SUGGESTION_PROMPT_TEMPLATE,
    FALLBACK_CHECKLIST
)
from src.config.constants import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
from src.utils.logger import log_api_call, log_error, safe_execute


class TripPlannerAgent:
    """
    AI Agent responsible for:
    - Creating comprehensive checklists
    - Brainstorming trip ideas
    - Providing suggestions
    - Managing pre-trip needs
    """

    def __init__(self, api_key: str, model: str = None):
        """
        Initialize the Trip Planner Agent with OpenAI

        Args:
            api_key: OpenAI API key
            model: Model to use (defaults to DEFAULT_MODEL from config)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model or DEFAULT_MODEL
        self.system_prompt = SYSTEM_PROMPT

    def generate_comprehensive_checklist(self, trip_details: TripDetails) -> List[ChecklistItem]:
        """
        Generate a comprehensive checklist based on trip details
        Includes obvious items and easily forgotten ones
        """
        phase = get_trip_phase(trip_details.start_date)
        days_until = (trip_details.start_date - datetime.now(pytz.UTC)).days

        # Build prompt from template
        prompt = CHECKLIST_PROMPT_TEMPLATE.format(
            destination=trip_details.destination,
            start_date=trip_details.start_date.strftime('%B %d, %Y'),
            days_until=days_until,
            party_size=trip_details.party_size,
            ages=', '.join(map(str, trip_details.ages)) if trip_details.ages else 'Not specified',
            interests=', '.join(trip_details.interests) if trip_details.interests else 'General Disney experience',
            budget_range=trip_details.budget_range or 'Not specified',
            special_needs=', '.join(trip_details.special_needs) if trip_details.special_needs else 'None',
            trip_phase=phase
        )

        try:
            log_api_call('OpenAI', 'chat.completions', {'model': self.model, 'purpose': 'checklist_generation'})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=MAX_TOKENS,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            # Parse the response - handle both direct array and object with items key
            data = json.loads(content)
            if isinstance(data, dict) and "items" in data:
                items_data = data["items"]
            elif isinstance(data, list):
                items_data = data
            else:
                items_data = list(data.values())[0] if data else []

            checklist = []
            for item in items_data:
                checklist.append(ChecklistItem(
                    id=generate_checklist_id(),
                    text=item.get("text", ""),
                    category=item.get("category", "general"),
                    priority=item.get("priority", "medium"),
                    deadline=item.get("deadline"),
                    completed=False
                ))

            log_api_call('OpenAI', 'chat.completions', response_summary=f"{len(checklist)} items generated")
            return checklist

        except Exception as e:
            log_error("Error generating checklist", e, {'trip_destination': trip_details.destination})
            return self._get_fallback_checklist()

    def brainstorm_ideas(self, trip_details: TripDetails, focus: str = "general") -> List[IdeaSuggestion]:
        """
        Brainstorm creative ideas and suggestions for the trip

        Args:
            trip_details: Trip information
            focus: Specific focus area (dining, activities, surprises, budget-friendly, etc.)
        """
        # Build prompt from template
        prompt = BRAINSTORMING_PROMPT_TEMPLATE.format(
            destination=trip_details.destination,
            start_date=trip_details.start_date.strftime('%B %d, %Y'),
            party_size=trip_details.party_size,
            ages=', '.join(map(str, trip_details.ages)) if trip_details.ages else 'Not specified',
            interests=', '.join(trip_details.interests) if trip_details.interests else 'All Disney experiences',
            budget_range=trip_details.budget_range or 'Not specified'
        )

        try:
            log_api_call('OpenAI', 'chat.completions', {'model': self.model, 'purpose': 'brainstorming'})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,  # Higher temperature for creativity
                max_tokens=MAX_TOKENS,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)
            ideas_data = data.get("ideas", [])

            ideas = []
            for idea in ideas_data:
                ideas.append(IdeaSuggestion(
                    id=generate_checklist_id(),
                    title=idea.get("title", ""),
                    description=idea.get("description", ""),
                    category=idea.get("category", "general"),
                    tags=idea.get("tags", []),
                    saved=False
                ))

            log_api_call('OpenAI', 'chat.completions', response_summary=f"{len(ideas)} ideas generated")
            return ideas

        except Exception as e:
            log_error("Error brainstorming ideas", e, {'trip_destination': trip_details.destination})
            return []

    def get_personalized_suggestion(self, trip_details: TripDetails, question: str) -> str:
        """
        Get a personalized suggestion or answer to a specific question
        """
        days_until = (trip_details.start_date - datetime.now(pytz.UTC)).days

        # Build prompt from template
        prompt = PERSONALIZED_SUGGESTION_PROMPT_TEMPLATE.format(
            question=question,
            destination=trip_details.destination,
            start_date=trip_details.start_date.strftime('%B %d, %Y'),
            days_until=days_until,
            party_size=trip_details.party_size,
            ages=', '.join(map(str, trip_details.ages)) if trip_details.ages else 'Not specified',
            interests=', '.join(trip_details.interests) if trip_details.interests else 'General',
            budget_range=trip_details.budget_range or 'Not specified'
        )

        try:
            log_api_call('OpenAI', 'chat.completions', {'model': self.model, 'purpose': 'personalized_suggestion'})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=MAX_TOKENS
            )

            return response.choices[0].message.content

        except Exception as e:
            log_error("Error getting personalized suggestion", e)
            return f"I apologize, but I encountered an error. Please try again later."

    def suggest_forgotten_items(self, current_checklist: List[ChecklistItem]) -> List[str]:
        """
        Analyze current checklist and suggest commonly forgotten items
        """
        current_items = [item.text for item in current_checklist]

        prompt = f"""Given this Disney trip checklist, what commonly forgotten items are missing?

Current checklist:
{json.dumps(current_items, indent=2)}

List 5-10 commonly forgotten items that aren't on this list. Focus on:
- Technology items (chargers, batteries, etc.)
- Comfort items (sunscreen, band-aids, etc.)
- Disney-specific items
- Travel documents or confirmations
- Weather-related items

Return as a simple JSON array of strings:
{{"forgotten_items": ["item 1", "item 2"]}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)
            return data.get("forgotten_items", [])

        except Exception as e:
            print(f"Error suggesting forgotten items: {e}")
            return []

    @staticmethod
    def parse_item_suggestions(response_text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Parse AI response for item suggestions and return cleaned text + suggested items

        Returns:
            Tuple of (cleaned_response_text, list_of_suggested_items)
            Each suggested item is a dict with keys: text, category, priority
        """
        # Pattern to match [ADD_ITEM: description | category | priority]
        pattern = r'\[ADD_ITEM:\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^\]]+)\s*\]'

        # Find all matches
        matches = re.findall(pattern, response_text)

        suggested_items = []
        for match in matches:
            description, category, priority = match
            suggested_items.append({
                'text': description.strip(),
                'category': category.strip().lower(),
                'priority': priority.strip().lower()
            })

        # Remove the [ADD_ITEM...] tags from the response text
        cleaned_text = re.sub(pattern, '', response_text)

        # Clean up any double spaces or newlines left behind
        cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)
        cleaned_text = re.sub(r'  +', ' ', cleaned_text)
        cleaned_text = cleaned_text.strip()

        return cleaned_text, suggested_items

    def _get_fallback_checklist(self) -> List[ChecklistItem]:
        """Fallback checklist if AI generation fails"""
        return [
            ChecklistItem(
                id=generate_checklist_id(),
                text=item["text"],
                category=item["category"],
                priority=item["priority"],
                completed=False
            )
            for item in FALLBACK_CHECKLIST
        ]
