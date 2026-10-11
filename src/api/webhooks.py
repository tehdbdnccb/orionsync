from fastapi import APIRouter, BackgroundTasks, Form, Request, status
from fastapi.responses import PlainTextResponse

from src.services.jobs import orchestrate_workflow

router = APIRouter()


@router.post("/twilio", status_code=status.HTTP_202_ACCEPTED)
async def twilio_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None),
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
        media_url=MediaUrl0 if NumMedia > 0 else None,
    )

    # 2. Immediately return an empty TwiML response to satisfy Twilio.
    # The reply is sent via the Twilio REST API by the notifications service.
    return PlainTextResponse(
        content="<Response></Response>",
        status_code=status.HTTP_202_ACCEPTED,
        media_type="application/xml",
    )

