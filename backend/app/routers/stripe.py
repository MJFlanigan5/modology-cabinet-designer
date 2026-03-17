"""Stripe Payment Integration Router

Handles subscriptions, one-time payments, and webhooks.
Set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET as environment variables.
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional, List
import stripe
import os
import json
from datetime import datetime

router = APIRouter(prefix="/api/stripe", tags=["payments"])

# Configure Stripe with environment variable
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Define subscription plans
SUBSCRIPTION_PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "stripe_price_id": None,  # No Stripe price for free tier
        "features": [
            "3 projects",
            "Basic cabinet templates",
            "Cut list generation",
            "Standard G-code export (GRBL only)",
            "Community support"
        ],
        "limits": {
            "projects": 3,
            "exports_per_month": 10,
            "cabinets_per_project": 10
        }
    },
    "hobbyist": {
        "name": "Hobbyist",
        "price": 9,
        "stripe_price_id": os.getenv("STRIPE_PRICE_HOBBYIST"),
        "features": [
            "Unlimited projects",
            "All cabinet templates",
            "Advanced waste optimization",
            "All G-code formats (ShopBot, Shapeoko, X-Carve, GRBL)",
            "3D exports (OBJ, STL, 3MF, DXF)",
            "Email support"
        ],
        "limits": {
            "projects": -1,  # Unlimited
            "exports_per_month": 50,
            "cabinets_per_project": -1
        }
    },
    "pro": {
        "name": "Pro",
        "price": 29,
        "stripe_price_id": os.getenv("STRIPE_PRICE_PRO"),
        "features": [
            "Everything in Hobbyist",
            "Advanced nesting (non-guillotine)",
            "Live hardware pricing from suppliers",
            "Project templates library",
            "Team collaboration (3 members)",
            "Priority support",
            "API access"
        ],
        "limits": {
            "projects": -1,
            "exports_per_month": -1,
            "cabinets_per_project": -1,
            "team_members": 3
        }
    },
    "shop": {
        "name": "Shop",
        "price": 79,
        "stripe_price_id": os.getenv("STRIPE_PRICE_SHOP"),
        "features": [
            "Everything in Pro",
            "Unlimited team members",
            "Custom branding on exports",
            "Priority hardware pricing",
            "Phone support",
            "Dedicated account manager",
            "Custom integrations"
        ],
        "limits": {
            "projects": -1,
            "exports_per_month": -1,
            "cabinets_per_project": -1,
            "team_members": -1
        }
    }
}


class CreateCheckoutSessionRequest(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str
    customer_email: Optional[str] = None


class CreatePortalSessionRequest(BaseModel):
    return_url: str
    customer_id: str


class SubscriptionStatus(BaseModel):
    plan: str
    status: str
    current_period_end: Optional[int] = None
    cancel_at_period_end: bool = False


@router.get("/plans")
async def get_plans():
    """Get all available subscription plans."""
    return {
        "plans": [
            {
                "id": plan_id,
                "name": plan["name"],
                "price": plan["price"],
                "price_id": plan["stripe_price_id"],
                "features": plan["features"],
                "limits": plan["limits"]
            }
            for plan_id, plan in SUBSCRIPTION_PLANS.items()
        ]
    }


@router.post("/create-checkout-session")
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """Create a Stripe checkout session for subscription."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            line_items=[
                {
                    "price": request.price_id,
                    "quantity": 1
                }
            ],
            success_url=request.success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.cancel_url,
            customer_email=request.customer_email,
            metadata={
                "source": "modology-cabinet-designer"
            }
        )
        
        return {
            "url": checkout_session.url,
            "session_id": checkout_session.id
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-portal-session")
async def create_portal_session(request: CreatePortalSessionRequest):
    """Create a Stripe billing portal session for subscription management."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=request.customer_id,
            return_url=request.return_url
        )
        
        return {
            "url": portal_session.url
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle different event types
    event_type = event["type"]
    
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: Update user's subscription in database
        # Extract customer_id, subscription_id, and update user record
        print(f"Checkout completed: {session}")
        
    elif event_type == "customer.subscription.created":
        subscription = event["data"]["object"]
        print(f"Subscription created: {subscription}")
        
    elif event_type == "customer.subscription.updated":
        subscription = event["data"]["object"]
        # TODO: Update user's subscription tier in database
        print(f"Subscription updated: {subscription}")
        
    elif event_type == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # TODO: Downgrade user to free tier
        print(f"Subscription cancelled: {subscription}")
        
    elif event_type == "invoice.paid":
        invoice = event["data"]["object"]
        print(f"Invoice paid: {invoice}")
        
    elif event_type == "invoice.payment_failed":
        invoice = event["data"]["object"]
        # TODO: Notify user of failed payment
        print(f"Payment failed: {invoice}")
    
    return {"status": "success"}


@router.get("/subscription/{customer_id}")
async def get_subscription_status(customer_id: str):
    """Get subscription status for a customer."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            status="active"
        )
        
        if subscriptions.data:
            sub = subscriptions.data[0]
            return SubscriptionStatus(
                plan=sub.metadata.get("plan", "unknown"),
                status=sub.status,
                current_period_end=sub.current_period_end,
                cancel_at_period_end=sub.cancel_at_period_end
            )
        
        return SubscriptionStatus(
            plan="free",
            status="inactive"
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel-subscription")
async def cancel_subscription(subscription_id: str):
    """Cancel a subscription at period end."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        
        return {
            "status": "success",
            "message": "Subscription will cancel at period end",
            "cancel_at": subscription.cancel_at
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reactivate-subscription")
async def reactivate_subscription(subscription_id: str):
    """Reactivate a cancelled subscription."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
        
        return {
            "status": "success",
            "message": "Subscription reactivated"
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices/{customer_id}")
async def get_invoices(customer_id: str, limit: int = 10):
    """Get invoice history for a customer."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        invoices = stripe.Invoice.list(
            customer=customer_id,
            limit=limit
        )
        
        return {
            "invoices": [
                {
                    "id": inv.id,
                    "number": inv.number,
                    "amount_paid": inv.amount_paid / 100,  # Convert from cents
                    "currency": inv.currency,
                    "status": inv.status,
                    "created": inv.created,
                    "invoice_pdf": inv.invoice_pdf
                }
                for inv in invoices.data
            ]
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-products")
async def create_stripe_products():
    """One-time setup: Create Stripe products and prices for all plans."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    created = []
    
    for plan_id, plan in SUBSCRIPTION_PLANS.items():
        if plan["price"] == 0:
            continue
        
        # Create product
        product = stripe.Product.create(
            name=f"Modology Cabinet Designer - {plan['name']}",
            description=f"\n".join(plan['features']),
            metadata={
                "plan_id": plan_id
            }
        )
        
        # Create price
        price = stripe.Price.create(
            product=product.id,
            unit_amount=plan["price"] * 100,  # Convert to cents
            currency="usd",
            recurring={
                "interval": "month"
            },
            metadata={
                "plan_id": plan_id
            }
        )
        
        created.append({
            "plan_id": plan_id,
            "product_id": product.id,
            "price_id": price.id,
            "price": plan["price"]
        })
    
    return {
        "status": "success",
        "message": "Products and prices created. Add these price IDs to your environment variables:",
        "products": created,
        "env_vars": {
            f"STRIPE_PRICE_{item['plan_id'].upper()}": item["price_id"]
            for item in created
        }
    }
