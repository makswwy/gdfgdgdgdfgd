from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import COMMUNITY_MESSAGES_LINK, MAIN_TEXT_RATES, RATES


_DURATION_LABELS = {
    3: "3 дня",
    7: "1 неделя",
    30: "1 месяц",
    90: "3 месяца",
    180: "6 месяцев",
    365: "1 год",
}


def _format_rate_label(days: int, price: int, *, promo: bool = False) -> str:
    duration = _DURATION_LABELS.get(int(days), f"{days} дн.")
    if promo:
        return f"🔥 Акция: {duration} — {price} ₽"
    return f"📌 {duration} — {price} ₽"


def _is_promo_rate(days: int, price: int) -> bool:
    return int(days) >= 180 or int(price) >= 3000


def _rate_color(days: int, price: int) -> str:
    return VkKeyboardColor.POSITIVE if _is_promo_rate(days, price) else VkKeyboardColor.PRIMARY


def _sorted_rates(rates: dict[int, dict]) -> list[tuple[int, dict]]:
    return sorted(rates.items(), key=lambda item: int(item[0]))


def generate_main_menu(has_active_ad: bool = False, has_messages: bool = False):
    keyboard = VkKeyboard(inline=True)

    if has_messages:
        keyboard.add_callback_button("📂 Мои объявления", color=VkKeyboardColor.PRIMARY, payload={"command": ".сообщение"})
        if has_active_ad:
            keyboard.add_callback_button("⏳ Продлить рекламу", color=VkKeyboardColor.POSITIVE, payload={"command": ".продлить"})
        keyboard.add_line()
        keyboard.add_openlink_button("🚀 Заказать ещё рекламу", link=COMMUNITY_MESSAGES_LINK)
        return keyboard.get_keyboard()

    keyboard.add_openlink_button("🚀 Купить рекламу", link=COMMUNITY_MESSAGES_LINK)
    keyboard.add_line()
    keyboard.add_callback_button("📋 Как это работает", color=VkKeyboardColor.SECONDARY, payload={"command": ".помощь"})
    keyboard.add_callback_button("ℹ️ О сервисе", color=VkKeyboardColor.SECONDARY, payload={"command": ".инфо_о_нас"})
    return keyboard.get_keyboard()


def generate_main_text_rates_menu():
    keyboard = VkKeyboard(inline=True)
    items = _sorted_rates(MAIN_TEXT_RATES)
    for index, (days, data) in enumerate(items, start=1):
        price = int(data.get("price", 0) or 0)
        keyboard.add_callback_button(
            _format_rate_label(int(days), price, promo=_is_promo_rate(int(days), price)),
            color=_rate_color(int(days), price),
            payload={"command": "buy_main_text", "days": days},
        )
        if index < len(items):
            keyboard.add_line()
    return keyboard.get_keyboard()


def generate_rates_menu():
    keyboard = VkKeyboard(inline=True)
    items = _sorted_rates(RATES)
    for index, (days, data) in enumerate(items, start=1):
        price = int(data.get("price", 0) or 0)
        keyboard.add_callback_button(
            _format_rate_label(int(days), price, promo=_is_promo_rate(int(days), price)),
            color=_rate_color(int(days), price),
            payload={"command": "rate_select", "days": days},
        )
        if index < len(items):
            keyboard.add_line()
    return keyboard.get_keyboard()


def generate_order_details_kb():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button("✅ Одобрить", color=VkKeyboardColor.POSITIVE, payload={"command": "approve_ui"})
    keyboard.add_callback_button("❌ Отклонить", color=VkKeyboardColor.NEGATIVE, payload={"command": "reject_ui"})
    keyboard.add_line()
    keyboard.add_callback_button("📎 Показать чек", color=VkKeyboardColor.SECONDARY, payload={"command": "show_check_ui"})
    keyboard.add_callback_button("🔙 Выйти", color=VkKeyboardColor.SECONDARY, payload={"command": "exit_ui"})
    return keyboard.get_keyboard()


def generate_exit_kb():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button("🔙 Выйти", color=VkKeyboardColor.SECONDARY, payload={"command": "exit_ui"})
    return keyboard.get_keyboard()
