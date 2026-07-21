from django.db import migrations, models
from django.utils.text import slugify


def generate_unique_category_slugs(apps, schema_editor):
    Category = apps.get_model("Products", "Category")
    for category in Category.objects.all():
        base_slug = slugify(category.title)  # ← مطمئن شو که فیلد title وجود داره
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exclude(pk=category.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        category.slug = slug
        category.save()


def generate_unique_product_slugs(apps, schema_editor):
    Product = apps.get_model("Products", "Products")
    for product in Product.objects.all():
        base_slug = slugify(product.title)  # ← مطمئن شو فیلد title در مدل Product هست
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        product.slug = slug
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0012_alter_color_color_code_alter_color_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(null=True, blank=True, unique=True),
        ),
        migrations.AddField(
            model_name="products",
            name="slug",
            field=models.SlugField(null=True, blank=True, unique=True),
        ),
        migrations.RunPython(generate_unique_category_slugs),
        migrations.RunPython(generate_unique_product_slugs),
    ]
