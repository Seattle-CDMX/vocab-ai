import json
import logging
from typing import Literal

from livekit.agents import get_job_context

logger = logging.getLogger("agent.terminal_state")


class TerminalStateManager:
    """Shared service for handling terminal states across all agents."""

    @staticmethod
    async def handle_terminal_state(
        state_type: Literal["success", "failure"],
        message: str,
        hint: str = "",
    ) -> None:
        """
        Handle terminal state for any agent by sending both toast notification 
        and session closure instruction to frontend.

        Args:
            state_type: Either "success" or "failure"
            message: The message to show in the toast
            hint: Optional hint for failure states
        """
        try:
            # Find the first remote participant (should be the student)
            participants = get_job_context().room.remote_participants.values()
            
            for participant in participants:
                participant_identity = participant.identity
                
                # Send toast notification RPC
                toast_payload = {
                    "type": state_type,
                    "message": message,
                }
                if hint and state_type == "failure":
                    toast_payload["hint"] = hint

                await get_job_context().room.local_participant.perform_rpc(
                    destination_identity=participant_identity,
                    method="show_toast",
                    payload=json.dumps(toast_payload),
                    response_timeout=1.0,
                )
                logger.info(f"📤 [TerminalState] Sent {state_type} toast to {participant_identity}")

                # Send session closure instruction RPC
                closure_payload = {
                    "action": "close_session",
                    "reason": "terminal_state_reached",
                    "state_type": state_type,
                }

                await get_job_context().room.local_participant.perform_rpc(
                    destination_identity=participant_identity,
                    method="close_session", 
                    payload=json.dumps(closure_payload),
                    response_timeout=1.0,
                )
                logger.info(f"📤 [TerminalState] Sent session closure instruction to {participant_identity}")
                
                # Only send to first participant
                break
                
        except Exception as e:
            logger.error(f"❌ [TerminalState] Failed to send terminal state RPCs: {e}")

    @staticmethod
    async def handle_success(message: str) -> None:
        """Convenience method for handling success terminal states."""
        await TerminalStateManager.handle_terminal_state("success", message)
        
    @staticmethod  
    async def handle_failure(message: str, hint: str = "") -> None:
        """Convenience method for handling failure terminal states."""
        await TerminalStateManager.handle_terminal_state("failure", message, hint)