def get_event_icon(event_name):

    event = event_name.lower()

    if any(word in event for word in ["ai", "openai", "chatgpt", "anthropic"]):
        return "🤖"

    elif any(word in event for word in ["football", "world cup", "fifa", "soccer"]):
        return "⚽"

    elif any(word in event for word in ["trump", "government", "election", "parliament"]):
        return "🏛️"

    elif any(word in event for word in ["iran", "israel", "ukraine", "war"]):
        return "🌍"

    elif any(word in event for word in ["apple", "google", "microsoft", "meta"]):
        return "💻"

    elif any(word in event for word in ["gta", "xbox", "playstation", "gaming"]):
        return "🎮"

    elif any(word in event for word in ["heat", "climate", "weather"]):
        return "🌡️"

    elif any(word in event for word in ["market", "economy", "business", "finance"]):
        return "💼"

    return "📰"