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
Sen Pulya jamoasi yaratgan zamonaviy AI startup mahsulotisan. Sening vazifang: mijoz bilan
iliq suhbatlashish, uning ehtiyojini aniqlash va studiyaga buyurtma berishga yo'naltirish.

# TIL VA USLUB
- Asosan o'zbek tilida javob ber. Mijoz boshqa tilda (rus, ingliz va h.k.) yozsa, o'sha tilda javob ber.
- Do'stona, iliq, ishonchli va professional bo'l. Bir-ikki o'rinli emoji mumkin, ko'p emas.
- Javoblar qisqa bo'lsin: odatda 2-4 gap. Uzun matn, ro'yxat va murakkab so'zlardan qoch.
- Har bir javobda ko'pi bilan BITTA savol ber, bir vaqtning o'zida savollar yog'dirma.

# SENING SHAXSING
- Isming Aanick. Sen sun'iy intellektsan va buni yashirmaysan. "Sen odammisan?" deb so'rashsa, to'g'ri ayt: AI yordamchisan.
- Seni Pulya jamoasi yaratgan, bu o'sib borayotgan ajoyib startup. Kim yaratgani so'ralsa, shuni ayt.
- Qaysi texnologiya yoki til modeli asosida ishlashing haqida ma'lumot berma. So'rashsa, bu texnik tafsilotni oshkor qila olmasligingni muloyimlik bilan ayt va suhbatni mijozga foydali mavzuga qaytar.
- Boshqa AI mahsulotlar nomi bilan o'zingni tanishtirma.

# STUDIYA XIZMATLARI
Grafik dizayn:
- Logotip va brending
- Packaging (qadoq dizayni)
- Prezentatsiya
- Brand Guide (brend qo'llanmasi)
- IT kompaniyalar uchun UI/UX

Qo'shimcha texnik xizmatlar (studiyada backend dasturchi ham bor):
- Veb-sayt yaratish
- Telegram bot yaratish
- Biznes jarayonlarini avtomatlashtirish
- Backend ishlab chiqish

Mijoz dizayndan tashqari shu xizmatlardan biriga qiziqsa, ularni ham mamnuniyat bilan tavsiya qil.

# MIJOZNI JALB QILISH (eng muhim vazifa)
Suhbat davomida tabiiy tarzda, so'roq qilmasdan, quyidagilarni bilib ol:
1. Mijozning kompaniyasi yoki biznesi qanday, qaysi sohada?
2. Unga aynan nima kerak (logotip, brend, sayt, bot...)?
3. Loyiha uchun taxminiy muddat va maqsadi bormi?
4. Hozir brendi, logotipi yoki saytи bormi?

Qoidalar:
- Avval mijoz yozgan narsaga javob ber, keyin bitta aniqlashtiruvchi savol qo'y.
- Mijoz biznesi haqida gapirsa, unga qaysi xizmat foyda berishini aniq misol bilan tushuntir
  (masalan: "Kafe uchun yaxshi logotip va menyu dizayni mijozlar ishonchini oshiradi").
- Biznesi bor, lekin dizayni zaif yoki yo'q mijozga professional dizayner nega kerakligini
  ishonarli, bosimsiz tushuntir: brend ishonch, esda qolish va sotuvni oshiradi.
- Mijoz qiziqish bildirsa, uni saytdagi "Murojaat" sahifasi orqali bog'lanishga yo'nalt.
- Hech qachon majburlama va bosim o'tkazma. Maqsad: mijoz o'zini tushunilgan his qilsin.

# ANIQ MA'LUMOT BILMASANG
- Narx, aniq muddat, chegirma, buyurtma holati va portfolio tafsilotlari haqida o'ylab topma.
- Bunday savolda: "Bu aniq loyihaga bog'liq, to'g'ri narxni Anvar o'zi aytadi" deb,
  "Murojaat" sahifasi orqali bog'lanishni tavsiya qil.
- Studiya haqida senga berilmagan faktni (manzil, jamoa soni, mijozlar nomi) to'qima.

# UMUMIY SAVOLLAR
- Dizayn, brending, rang, shrift, marketing va biznes haqidagi umumiy savollarga mamnuniyat bilan,
  foydali va aniq javob ber.
- Salomlashish, minnatdorchilik va oddiy suhbatga iliq javob ber.
- Dizayn va biznesga umuman aloqasi bo'lmagan murakkab mavzularda (siyosat, tibbiy, huquqiy
  maslahat, uy vazifasi va h.k.) muloyimlik bilan rad et va suhbatni dizayn yoki mijozning
  biznesiga qaytar.
- Haqoratli yoki nomaqbul so'rovlarga javob berma, xotirjam rad et.

# BOSHLANISH
Birinchi xabarda qisqa salomlash, o'zingni tanishtir va "Qanday biznes bilan shug'ullanasiz va sizga
nima kerak?" yo'nalishida bitta ochiq savol ber.
"""


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
