import json
import logging

from livekit.agents import AgentSession

from models.session import MySessionInfo, create_target_lexical_item

logger = logging.getLogger("agent.handlers")


def process_participant_voice_card_data(participant, session: AgentSession):
    """Process participant voice card data and update session."""
    logger.info(f"🎯 [Agent] Processing participant: {participant.identity}")
    logger.info(f"🎯 [Agent] All participant attributes: {participant.attributes}")

    # Get voice card data from participant attributes
    voice_card_json = participant.attributes.get("voice_card_data")
    logger.info(f"🎯 [Agent] Voice card JSON received: {voice_card_json}")

    session_info = session.userdata

    if voice_card_json:
        try:
            voice_card = json.loads(voice_card_json)
            logger.info(
                f"🎯 [Agent] Parsed voice card data successfully: {voice_card['title']}"
            )
            logger.info(f"🎯 [Agent] Voice card type: {voice_card['type']}")
            logger.info(f"🎯 [Agent] Full voice card object: {voice_card}")

            # Extract phrasal verb data from voice card
            phrasal_verb = voice_card["targetPhrasalVerb"]
            verb = phrasal_verb["verb"]
            senses = phrasal_verb["senses"]

            logger.info(f"🎯 [Agent] Extracted verb: {verb}")
            logger.info(f"🎯 [Agent] Extracted senses: {senses}")

            # Create target lexical item from voice card data
            target_item = create_target_lexical_item(verb, senses)
            logger.info(
                f"🎯 [Agent] Created target lexical item with {target_item.total_senses} senses"
            )

            # Update session info with dynamic data
            if isinstance(session_info, MySessionInfo):
                session_info.target_lexical_item = target_item
                session.userdata = session_info

            logger.info(
                f"🎯 [Agent] ✅ COMPLETE: Updated session with voice card data for: {verb}"
            )

            # Now start the conversation with the voice card data
            instructions = f"""The TARGET LEXICAL ITEM IS '{target_item.phrase}'. This phrasal verb has {target_item.total_senses} different meanings. 

Ask the user to explain what this phrasal verb means. When they explain a meaning, determine which of the {target_item.total_senses} senses they are explaining and whether it's correct.

The {target_item.total_senses} senses are:
"""
            for sense in target_item.senses:
                instructions += f"{sense.sense_number}. {sense.definition} (Example: {sense.examples[0]})\n"

            instructions += (
                f"\nStart by asking them to explain what '{target_item.phrase}' means."
            )

            logger.info(
                f"🎯 [Agent] 🗣️ Starting conversation about: {target_item.phrase}"
            )
            session.generate_reply(instructions=instructions)

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"🎯 [Agent] ❌ Failed to parse voice card data: {e}")
            logger.error(f"🎯 [Agent] Raw JSON that failed: {voice_card_json}")
            # Fallback: create a simple target item
            fallback_data = [
                {
                    "senseNumber": 1,
                    "definition": "Practice phrasal verb",
                    "examples": ["Example sentence"],
                }
            ]
            if isinstance(session_info, MySessionInfo):
                session_info.target_lexical_item = create_target_lexical_item(
                    "PRACTICE VERB", fallback_data
                )
                session.userdata = session_info
            logger.info("🎯 [Agent] Using fallback data: PRACTICE VERB")
            session.generate_reply(
                instructions="I couldn't get the voice card data. Let me ask you about a practice phrasal verb instead."
            )
    else:
        logger.warning(
            "🎯 [Agent] ❌ No voice card data found in participant attributes"
        )
        logger.warning(
            f"🎯 [Agent] Available attribute keys: {list(participant.attributes.keys())}"
        )
        # Fallback: create a simple target item
        fallback_data = [
            {
                "senseNumber": 1,
                "definition": "Practice phrasal verb",
                "examples": ["Example sentence"],
            }
        ]
        if isinstance(session_info, MySessionInfo):
            session_info.target_lexical_item = create_target_lexical_item(
                "PRACTICE VERB", fallback_data
            )
            session.userdata = session_info
        logger.info("🎯 [Agent] Using fallback data: PRACTICE VERB")
        session.generate_reply(
            instructions="I'm waiting for voice card data. Please ensure your connection includes the phrasal verb information."
        )
