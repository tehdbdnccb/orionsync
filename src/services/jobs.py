# from src.adapters.openai_client import transcribe_audio
# from src.adapters.stripe_client import create_invoice_link
from src.services.notifications import send_worker_update
from src.services.text import extract_intent_and_entities
# from src.utils.logger import log


def orchestrate_workflow(sender: str, body: str, media_url: str = None):
    """
    The main execution thread for an inbound worker request.
    Handles transcription, extraction, business routing, and the final user response.
    """
    try:
        # Step 1: Normalize Input
        working_text = body
        if media_url:
            # log.info(f"Downloading and transcribing media from {media_url}")
            # working_text = transcribe_audio(media_url)
            working_text = "I'm on the A104 with truck KCD 456X. Axle is snapped. Dispatch a tow and quote 45,000 for the heavy-duty replacement."

        if not working_text:
            send_worker_update(sender, "⚠️ I didn't catch that. Could you send the text or voice note again?")
            return

        # Step 2: Extract Structured Data
        action_plan = extract_intent_and_entities(working_text)
        # log.info(f"Action parsed: {action_plan.intent} for {action_plan.client_or_vehicle_id}")

        # Step 3: Route to specific business logic based on intent
        response_message = ""

        if action_plan.intent == "dispatch_unit":
            # Mock API call to fleet management / database
            response_message = (
                f"✅ *Dispatch Confirmed*\n"
                f"Tow unit assigned to {action_plan.client_or_vehicle_id} at {action_plan.location}.\n"
                f"ETA: 45 minutes."
            )

            # Chain actions: If they mentioned a cost, generate an invoice instantly
            if action_plan.total_cost:
                # invoice_url = create_invoice_link(action_plan.total_cost, action_plan.items)
                invoice_url = "https://pay.mock-stripe.com/inv_123"
                response_message += f"\n\n🧾 *Client Invoice Generated*:\n{invoice_url}"

        elif action_plan.intent == "order_parts":
            # Mock API call to supplier inventory
            parts_list = "\n- ".join(action_plan.items)
            response_message = f"📦 *Order Placed*:\n- {parts_list}\nThese will be ready at the depot by 08:00 tomorrow."

        else:
            response_message = f"Done. Logged update for {action_plan.client_or_vehicle_id}."

        # Step 4: Close the loop with the worker
        send_worker_update(sender, response_message)

    except Exception:
        # log.error(f"Workflow failed: {str(e)}")
        send_worker_update(sender, "❌ System encountered an error processing that request. Please contact dispatch.")

