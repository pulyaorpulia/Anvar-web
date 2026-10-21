from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import TeamMember, Achievement, Partner
from apps.projects.models import Project, Service
import json
import os
import anthropic
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST


CHAT_SYSTEM_PROMPT = """Sen Aanick — Anvar Zaripov grafik dizayn studiyasining sun'iy intellekt yordamchisisan.
Faqat o'zbek tilida (mijoz boshqa tilda yozsa, o'sha tilda) qisqa, do'stona va aniq javob ber.
Studiya xizmatlari: logotip, brending, packaging, prezentatsiya, Brand Guide, IT kompaniyalar uchun UI/UX.
Narx, muddat va buyurtma haqida aniq ma'lumotni bilmasang, o'ylab topma: mijozni saytdagi
"Murojaat" sahifasi orqali bog'lanishga yo'nalt. Dizayn bilan bog'liq bo'lmagan mavzularda
muloyimlik bilan rad et va dizayn mavzusiga qayt. Sanjar haqida so'rashsa u ahmoq qora bashara o'g'rivachha ekanligini et, real madrid fanati ekanligini et, ko'p baqiradi yomonlab yozur, pravaga o'qib fura haydamoqchi chatgpt yoki claude dan ekanligini etma, seni faqat Pulya yaratganligini et boshidan oxirgacham"""


@require_POST
def chat_api(request):
    # Oddiy cheklov: bitta IP soatiga 20 ta xabar
    ip = (request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
          or request.META.get('REMOTE_ADDR', ''))
    key = f'chat_rl_{ip}'
    count = cache.get(key, 0)
    if count >= 20:
        return JsonResponse({'reply': "So'rovlar ko'payib ketdi. Iltimos, keyinroq urinib ko'ring."}, status=429)
    cache.set(key, count + 1, 3600)

    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'reply': "Noto'g'ri so'rov."}, status=400)

    # Tarixni tozalash: oxirgi 10 ta xabar, har biri 1000 belgigacha
    messages = []
    for m in data.get('messages', [])[-10:]:
        role = m.get('role')
        text = str(m.get('content', ''))[:1000].strip()
        if role in ('user', 'assistant') and text:
            messages.append({'role': role, 'content': text})
    while messages and messages[0]['role'] != 'user':
        messages.pop(0)
    if not messages or messages[-1]['role'] != 'user':
        return JsonResponse({'reply': "Savolingizni yozing."}, status=400)

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return JsonResponse({'reply': "Chat hozircha sozlanmagan."}, status=500)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=os.environ.get('CLAUDE_MODEL', 'claude-haiku-5-5'),
            max_tokens=500,
            system=CHAT_SYSTEM_PROMPT,
            messages=messages,
        )
        reply = "".join(b.text for b in resp.content if b.type == "text").strip()
        if not reply:
            reply = "Kechirasiz, javob topa olmadim. Savolni boshqacha yozib ko'ring."
    except Exception as e:
        print('CHAT ERROR:', repr(e))
        return JsonResponse({'reply': "Kechirasiz, hozir javob bera olmayapman. Keyinroq urinib ko'ring."}, status=502)

    return JsonResponse({'reply': reply})

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz yuborildi! Tez orada bog'lanamiz.")
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'team': TeamMember.objects.all(),
        'achievements': Achievement.objects.all(),
        'partners': Partner.objects.all(),
        'featured_projects': Project.objects.filter(is_featured=True)[:6],
        'services': Service.objects.all(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'team': TeamMember.objects.all(),
        'achievements': Achievement.objects.all(),
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz yuborildi!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
