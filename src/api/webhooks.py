from fastapi import APIRouter, BackgroundTasks, Form, Request, status
from fastapi.responses import PlainTextResponse

# In a full implementation, this imports from src/services/jobs.py
# from src.services.jobs import orchestrate_workflow

router = APIRouter()

def orchestrate_workflow(sender: str, body: str, media_url: str = None):
    """
    Mock dispatcher for Layer 2. 
    This function will call OpenAI, parse intents, and trigger Stripe.
    """
    print(f"[DISPATCH] Processing task for {sender} | Audio attached: {bool(media_url)}")
    # Logic executes here asynchronously...

@router.post("/twilio", status_code=status.HTTP_202_ACCEPTED)
async def twilio_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None)
):
    """
    Ingests incoming WhatsApp messages and media.
    Uses BackgroundTasks to prevent Twilio from timing out while the LLM runs.
    """
    
    # 1. Dispatch the actual AI and business logic to a background worker
    background_tasks.add_task(
        orchestrate_workflow,
        sender=From,
        body=Body,
        media_url=MediaUrl0 if NumMedia > 0 else None
    )

    # 2. Immediately return an empty TwiML response to satisfy Twilio.
    # If we don't return XML, Twilio logs a warning in the console.
    # The actual reply will be sent via the Twilio REST API by our service layer later.
    return PlainTextResponse(
        content="<Response></Response>", 
        media_type="application/xml"
    )