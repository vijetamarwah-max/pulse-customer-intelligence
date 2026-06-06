import json

from .agent import EventUnderstandingAgent


def main() -> None:
    agent = EventUnderstandingAgent()

    events = {
        "raw_events": [
            "product_view",
            "product_view",
            "search",
            "add_to_cart",
            "cart_abandoned",
        ],
        "view_count": 8,
        "cart_actions": 2,
        "checkout_actions": 0,
        "session_depth": 5,
    }

    user_state = {
        "inactive_days": 3,
        "recent_complaint": False,
        "events_7d": 6,
        "cart_actions_30d": 2,
    }

    output = agent.run("U123", events, user_state)

    if hasattr(output, "model_dump"):
        payload = output.model_dump()
    else:
        payload = output.dict()

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
