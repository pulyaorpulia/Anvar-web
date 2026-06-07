from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    """Xizmat turlari: Logotip, Brending, Packaging..."""
    icon = models.CharField(max_length=100, verbose_name="Icon")
    title = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(verbose_name="Tavsifi")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"

    def __str__(self):
        return self.title


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('logo', 'Logotip'),
        ('branding', 'Brending'),
        ('packaging', 'Packaging'),
        ('presentation', 'Prezentatsiya'),
        ('other', 'Boshqa'),
    ]

    title = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="Kategoriya"
    )
    description = models.TextField(verbose_name="To'liq tavsif")
    short_description = models.CharField(max_length=300, verbose_name="Qisqa tavsif")
    image = models.ImageField(upload_to='projects/', verbose_name="Asosiy rasm")
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifada ko'rsatish")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # avtomatik slug yasaydi
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image_gallery = models.ImageField(upload_to='projects/gallery/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Loyiha rasmi"
        verbose_name_plural = "Loyiha rasmlari"