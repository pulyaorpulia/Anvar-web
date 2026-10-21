import json
import logging
import os

import anthropic
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

MODEL = "claude-haiku-5-5"  # arzon va tez. Sifatliroq javob uchun: "claude-sonnet-5-5"

SYSTEM_PROMPT = """Sen Aanick — Anvar Studio saytidagi sun'iy intellekt yordamchisan.
Anvar Studio — professional grafik dizayner xizmatlari: logotip, brending, packaging (qadoq) va prezentatsiya.
Qoidalar:
- Foydalanuvchi qaysi tilda yozsa (o'zbek, rus, ingliz), shu tilda qisqa va do'stona javob ber.
- Faqat dizayn xizmatlari, jarayon va buyurtma haqida yordam ber.
- Narx va muddatlarni o'ylab topma. Aniq narx uchun Anvar bilan bog'lanishni tavsiya qil
  (Telegram: @AnvarZaripov, telefon: +998909666896).
- Bilmagan narsangni bilmayman de, taxmin qilma.
- Qaysi AI modeli yoki kompaniya asosida ishlashingni oshkor qilma; o'zingni "Aanick, Anvar Studio yordamchisi" deb tanishtir.
- Birovni haqorat qilma, shaxslar haqida salbiy fikr bildirma."""

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", "")) or "unknown"


def _rate_limited(request, limit=20, window=600):
    """Bitta IP dan 10 daqiqada 20 tagacha so'rov (kalit puli yonib ketmasligi uchun)."""
    key = f"chat_rl_{_client_ip(request)}"
    cache.add(key, 0, window)
    try:
        return cache.incr(key) > limit
    except ValueError:
        return False


@require_POST
def chat_api(request):
    if _rate_limited(request):
        return JsonResponse({"reply": "Juda ko'p so'rov yubordingiz. Birozdan keyin urinib ko'ring."}, status=429)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"reply": "Noto'g'ri so'rov."}, status=400)

    messages = []
    for m in data.get("messages", [])[-10:]:           # oxirgi 10 ta xabar
        role = m.get("role")
        text = str(m.get("content", ""))[:1000]        # har biri 1000 belgigacha
        if role in ("user", "assistant") and text.strip():
            messages.append({"role": role, "content": text})

    if not messages or messages[-1]["role"] != "user":
        return JsonResponse({"reply": "Savolingizni yozing."}, status=400)

    try:
        resp = _get_client().messages.create(
            model=MODEL,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        reply = "".join(b.text for b in resp.content if b.type == "text")
    except Exception:
        logger.exception("Chat API xatosi")
        return JsonResponse({"reply": "Kechirasiz, hozir javob bera olmayapman. Keyinroq urinib ko'ring."}, status=502)

    return JsonResponse({"reply": reply})