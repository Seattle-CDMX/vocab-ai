import asyncio
import json
import logging
from typing import Literal

from livekit.agents import get_job_context

logger = logging.getLogger("agent.terminal_state")


class TerminalStateManager:
    """Shared service for handling terminal states across all agents with graceful session closure."""

    @staticmethod
    async def handle_terminal_state(
        state_type: Literal["success", "failure"],
        message: str,
        hint: str = "",
        delay_seconds: float = 4.0,
    ) -> None:
        """
        Handle terminal state for any agent by sending immediate toast notification
        and delayed session closure instruction to frontend.

        Args:
            state_type: Either "success" or "failure"
            message: The message to show in the toast
            hint: Optional hint for failure states
            delay_seconds: Delay before closing session (allows agent to finish speaking)
        """
        try:
            # Find the first remote participant (should be the student)
            participants = get_job_context().room.remote_participants.values()

            for participant in participants:
                participant_identity = participant.identity

                # Send immediate toast notification for user feedback
                await TerminalStateManager._send_toast_notification(
                    participant_identity, state_type, message, hint
                )

                # Schedule delayed session closure to allow agent to finish speaking
                asyncio.create_task(  # noqa: RUF006
                    TerminalStateManager._send_delayed_session_closure(
                        participant_identity, state_type, delay_seconds
                    )
                )

                # Only send to first participant
                break

        except Exception as e:
            logger.error(f"❌ [TerminalState] Failed to send terminal state RPCs: {e}")

    @staticmethod
    async def _send_toast_notification(
        participant_identity: str,
        state_type: str,
        message: str,
        hint: str = "",
    ) -> None:
        """Send immediate toast notification for user feedback."""
        try:
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
            logger.info(f"📤 [TerminalState] Sent immediate {state_type} toast to {participant_identity}")

        except Exception as e:
            logger.error(f"❌ [TerminalState] Failed to send toast notification: {e}")

    @staticmethod
    async def _send_delayed_session_closure(
        participant_identity: str,
        state_type: str,
        delay_seconds: float,
    ) -> None:
        """Send delayed session closure instruction after agent finishes speaking."""
        try:
            # Wait for agent to finish speaking
            logger.info(f"⏰ [TerminalState] Waiting {delay_seconds}s before closing session to allow agent to finish speaking")
            await asyncio.sleep(delay_seconds)

            # Send session closure instruction
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
            logger.info(f"📤 [TerminalState] Sent delayed session closure instruction to {participant_identity} after {delay_seconds}s")

        except Exception as e:
            logger.error(f"❌ [TerminalState] Failed to send delayed session closure: {e}")

    @staticmethod
    async def handle_success(message: str, delay_seconds: float = 4.0) -> None:
        """Convenience method for handling success terminal states with graceful closure."""
        await TerminalStateManager.handle_terminal_state("success", message, delay_seconds=delay_seconds)

    @staticmethod
    async def handle_failure(message: str, hint: str = "", delay_seconds: float = 3.0) -> None:
        """Convenience method for handling failure terminal states with graceful closure."""
        await TerminalStateManager.handle_terminal_state("failure", message, hint, delay_seconds)

