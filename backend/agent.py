from typing import Dict, Any
from llm_utils import extract_intent_entities
from calendar_utils import check_availability, create_event
import datetime

# Session state can be extended as needed

def extract_value(val):
    if isinstance(val, dict) and "value" in val:
        return val["value"]
    return val

def agent_respond(user_message: str, session_state: Dict[str, Any] = None) -> Dict[str, Any]:
    if session_state is None:
        session_state = {}

    # Step 1: Extract intent and entities
    llm_result = extract_intent_entities(user_message)
    intent = llm_result.get('intent', 'unknown')
    entities = llm_result.get('entities', {})
    print("Entities received from LLM:", entities)  # Debug print
    response = ""

    # Step 2: Handle intents
    if intent == 'book_appointment':
        # Extract required entities
        date = extract_value(entities.get('date'))
        time = extract_value(entities.get('time'))
        summary = entities.get('summary', 'Appointment')
        participants = entities.get('participants', [])
        description = entities.get('description', '')
        if date: date = str(date).strip()
        if time: time = str(time).strip()
        if not date or not time:
            response = "Could you please specify the date and time for the appointment?"
        else:
            # Parse date and time
            try:
                start_dt = datetime.datetime.fromisoformat(f"{date}T{time}")
                end_dt = start_dt + datetime.timedelta(hours=1)  # Default to 1 hour
                available = check_availability(start_dt, end_dt)
                if available:
                    event = create_event(summary, start_dt, end_dt, description, participants)
                    response = f"Your appointment has been booked for {start_dt.strftime('%A, %B %d at %I:%M %p')}!"
                else:
                    response = f"Sorry, that time is not available. Would you like to try a different time?"
            except Exception as e:
                print("Date/time parsing error:", e)
                response = f"I couldn't understand the date or time. Please provide them in YYYY-MM-DD and HH:MM format."
    elif intent == 'check_availability':
        date = extract_value(entities.get('date'))
        time = extract_value(entities.get('time'))
        if date: date = str(date).strip()
        if time: time = str(time).strip()
        if not date or not time:
            response = "Please specify the date and time you'd like to check."
        else:
            try:
                start_dt = datetime.datetime.fromisoformat(f"{date}T{time}")
                end_dt = start_dt + datetime.timedelta(hours=1)
                available = check_availability(start_dt, end_dt)
                if available:
                    response = f"The slot on {start_dt.strftime('%A, %B %d at %I:%M %p')} is available!"
                else:
                    response = f"That slot is not available. Would you like to check another time?"
            except Exception as e:
                print("Date/time parsing error:", e)
                response = f"I couldn't understand the date or time. Please provide them in YYYY-MM-DD and HH:MM format."
    else:
        response = "I'm here to help you book or check appointments. How can I assist you today?"

    # Update session state as needed (extend for multi-turn)
    session_state['last_intent'] = intent
    session_state['entities'] = entities

    return {"response": response, "session_state": session_state}
