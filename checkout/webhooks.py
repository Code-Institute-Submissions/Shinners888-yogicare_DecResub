from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhookHandler import StripeWebhookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    # Stripe web handler setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # verify webhook
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
                payload, sig_header, wh_secret
                )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    handler = StripeWebhookHandler(request)

    # Map webhook event to related handler function
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_payment_failed,
    }

    # Get webhook Stripe
    event_type = event['type']

    # Use generic handler by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call event handler with event
    response = event_handler(event)
    return response
