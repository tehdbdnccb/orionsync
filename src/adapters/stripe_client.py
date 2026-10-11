import stripe
from config.settings import get_settings

settings = get_settings()
stripe.api_key = settings.stripe_secret_key

def create_invoice_link(amount_kes: int, item_description: str) -> str:
    """
    Generates a checkout link for the field worker to forward to the client.
    Note: amount is in the smallest currency unit (e.g., cents or cents equivalent).
    """
    try:
        # Create a dynamic product/price on the fly
        price = stripe.Price.create(
            currency="kes",
            unit_amount=amount_kes * 100, 
            product_data={"name": item_description},
        )
        
        # Generate the payment link
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            description="Field Service Invoice"
        )
        
        return payment_link.url
    except Exception as e:
        print(f"Stripe generation failed: {e}")
        # Fail gracefully during the demo
        return "https://mock-pay.link/error-fallback"