import json
import logging

from livekit.agents import AgentSession

from models.session import MySessionInfo, create_target_lexical_item

logger = logging.getLogger("agent.handlers")


def process_participant_data(participant, session: AgentSession):
    """Process participant data and return appropriate agent based on activity type."""
    logger.info(f"🎯 [Agent] Processing participant: {participant.identity}")
    logger.info(f"🎯 [Agent] All participant attributes: {participant.attributes}")

    # Try to get metadata from token (unified approach)
    metadata_json = None
    if hasattr(participant, "metadata") and participant.metadata:
        metadata_json = participant.metadata
        logger.info(f"🎯 [Agent] Metadata from token: {metadata_json}")
    else:
        # Fallback to participant attributes (old approach for voice cards)
        voice_card_json = participant.attributes.get("voice_card_data")
        if voice_card_json:
            metadata_json = json.dumps(
                {"activityType": "voice", "voiceCardData": json.loads(voice_card_json)}
            )
        logger.info(
            f"🎯 [Agent] Voice card JSON from attributes (legacy fallback): {voice_card_json}"
        )

    session_info = session.userdata

    # Determine which agent to use based on metadata
    if metadata_json:
        try:
            metadata = json.loads(metadata_json)
            activity_type = metadata.get("activityType", "voice")
            logger.info(f"🎯 [Agent] Activity type: {activity_type}")
            logger.info(f"🎯 [Agent] Full metadata: {metadata}")

            # Return the appropriate agent based on activity type
            if activity_type == "context":
                # Context-based practice with role-playing
                from agents.context_agent import ContextAgent

                scenario_data = metadata.get("scenario", {})
                target_phrasal = metadata.get("targetPhrasalVerb", {})

                # Merge target phrasal verb info into scenario
                scenario_data["phrasalVerb"] = target_phrasal.get("verb", "go on")

                logger.info(
                    f"🎭 [Agent] Creating ContextAgent for scenario: {scenario_data.get('character')}"
                )
                return ContextAgent(scenario_data=scenario_data)

            else:
                # Default to voice card explanation mode
                voice_card_data = metadata.get("voiceCardData")
                if not voice_card_data:
                    # For legacy format
                    voice_card_data = metadata

                logger.info(
                    f"🎯 [Agent] Processing as voice card: {voice_card_data.get('title', 'Unknown')}"
                )

                # Extract phrasal verb data from voice card
                phrasal_verb = voice_card_data["targetPhrasalVerb"]
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

                # Return the NativeExplainAgent for voice card mode
                # The agent will access the session data and start the conversation
                from agents.native_explain_agent import NativeExplainAgent

                return NativeExplainAgent()

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"🎯 [Agent] ❌ Failed to parse metadata: {e}")
            logger.error(f"🎯 [Agent] Raw JSON that failed: {metadata_json}")
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

            # Return default agent - it will handle the fallback
            from agents.native_explain_agent import NativeExplainAgent

            return NativeExplainAgent()
    else:
        logger.warning(
            "🎯 [Agent] ❌ No metadata found in token or participant attributes"
        )
        logger.warning(
            f"🎯 [Agent] Available attribute keys: {list(participant.attributes.keys())}"
        )
        logger.warning(
            f"🎯 [Agent] Participant metadata: {getattr(participant, 'metadata', 'None')}"
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

        # Return default agent - it will handle the fallback
        from agents.native_explain_agent import NativeExplainAgent

        return NativeExplainAgent()
