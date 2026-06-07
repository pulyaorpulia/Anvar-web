from django.db import models


class SiteSettings(models.Model):
    """Admin paneldan telefon, manzil, ijtimoiy tarmoqlar boshqariladi"""
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    phone2 = models.CharField(max_length=20, blank=True, verbose_name="Telefon 2")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=500, verbose_name="Manzil")
    telegram = models.URLField(blank=True, verbose_name="Telegram")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    hero_image = models.ImageField(upload_to='site/', blank=True, verbose_name="Hero rasmi")
    about_image = models.ImageField(upload_to='site/', blank=True, verbose_name="Haqimda rasmi")
    logo = models.ImageField(upload_to='site/', blank=True, verbose_name="Logotip")
    favicon = models.ImageField(upload_to='site/', blank=True, verbose_name="Favicon")
    # Google Maps embed linki
    map_embed_url = models.TextField(blank=True, verbose_name="Xarita embed URL")
    demo_video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Demo video")


    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"


class TeamMember(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ismi")
    role = models.CharField(max_length=255, verbose_name="Lavozimi")
    photo = models.ImageField(upload_to='team/', verbose_name="Rasmi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")  # kim birinchi chiqishini boshqarish uchun

    class Meta:
        ordering = ['order']
        verbose_name = "Jamoa a'zosi"
        verbose_name_plural = "Jamoa"

    def __str__(self):
        return self.name


class Achievement(models.Model):
    """Yutuqlar: '150+ loyiha', '5 yil tajriba' kabi"""
    icon = models.CharField(max_length=100, verbose_name="Icon (emoji yoki FontAwesome class)")
    number = models.CharField(max_length=50, verbose_name="Raqam", help_text="Masalan: 150+")
    label = models.CharField(max_length=255, verbose_name="Tavsif", help_text="Masalan: Bajarilgan loyihalar")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Yutuq"
        verbose_name_plural = "Yutuqlar"

    def __str__(self):
        return f"{self.number} {self.label}"


class Partner(models.Model):
    """Hamkorlar — IT kompaniyalar"""
    name = models.CharField(max_length=255, verbose_name="Kompaniya nomi")
    logo = models.ImageField(upload_to='partners/', verbose_name="Logotipi")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ism")  # ✅ ismingiz → name
    email = models.EmailField(verbose_name="Email")  # ✅ pochtangiz → email
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")  # ➕ yangi
    message = models.TextField(verbose_name="Xabar")  # ✅ xabar → message
    is_read = models.BooleanField(default=False, verbose_name="O'qildi")  # ➕ admin uchun foydali
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"

    def __str__(self):
        return f"{self.name} — {self.email}"