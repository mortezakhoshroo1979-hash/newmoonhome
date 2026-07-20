from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import SiteSetting
from products.models import Product, ProductThreeD


class SiteConfigAPIView(APIView):
    def get(self, request, *args, **kwargs):
        site, _ = SiteSetting.objects.get_or_create(site_name="NEWMOON HOME")
        cfg = site.lovable_config or {}

        # Default brand
        brand = cfg.get("brand", {
            "name": site.site_name or "NEWMOON HOME",
            "tagline": site.site_description or "Luxury Furniture · Woodcraft · Bespoke Interiors",
            "logoInitial": "N",
        })

        # Default hero
        hero = cfg.get("hero", {
            "badge": "EST. DESIGN HOUSE · 2026 LUXURY COLLECTION",
            "title1": "خانه را با زبان طراحی",
            "title2Highlight": "لوکس و ماندگار",
            "title3": "بازآفرینی کنید",
            "subtitle": "NEWMOON HOME تجربه‌ای ممتاز از مبلمان، چوب‌های کمیاب، جزئیات ظریف دست‌ساز و امکان شخصی‌سازی کامل با چرخش ۳۶۰ درجه و واقعیت افزوده (AR) را در اختیار شما می‌گذارد.",
            "ctaPrimary": "مشاهده کالکشن ممتاز",
            "ctaSecondary": "استعلام ساخت اختصاصی",
            "stats": [
                ["+۱۲۰", "طرح سفارشی"],
                ["۳بعدی", "مشاهده با دوربین AR"],
                ["۱۰۰٪", "چوب طبیعی ممتاز"],
            ],
            "backgroundImage": request.build_absolute_uri("/static/assets/logo.png") if not site.logo else request.build_absolute_uri(site.logo.url),
        })

        # Default nav
        nav = cfg.get("nav", [
            {"label": "خانه", "href": "/"},
            {"label": "محصولات", "href": "/products/"},
            {"label": "درباره ما", "href": "/about/"},
            {"label": "ژورنال", "href": "/blog/"},
            {"label": "تماس با ما", "href": "/contact/"},
        ])

        # Categories
        categories = cfg.get("categories", [
            {"key": "living", "label": "مبلمان نشیمن"},
            {"key": "bedroom", "label": "سرویس خواب"},
            {"key": "table", "label": "میز و کنسول"},
        ])

        # Products list matching Lovable Product type
        db_products = Product.objects.select_related("category").filter(is_active=True)
        products_list = []
        for p in db_products:
            cat_key = "living"
            if p.category and ("bed" in p.category.slug.lower() or "خواب" in p.category.name):
                cat_key = "bedroom"
            elif p.category and ("table" in p.category.slug.lower() or "میز" in p.category.name):
                cat_key = "table"

            img_url = "/static/assets/logo.png"
            first_img = p.images.first()
            if first_img and first_img.image:
                img_url = request.build_absolute_uri(first_img.image.url)

            m_id = None
            first_3d = p.three_d_files.filter(is_active=True).first()
            if first_3d:
                m_id = str(first_3d.id)

            products_list.append({
                "id": str(p.id),
                "name": p.name,
                "tagline": p.description[:100] if p.description else "",
                "price": f"{p.current_price:,} ریال",
                "image": img_url,
                "signature": p.is_featured,
                "category": cat_key,
                "modelId": m_id,
            })

        # Models list matching Lovable Model3D type
        db_models = ProductThreeD.objects.filter(is_active=True)
        models_list = []
        for m in db_models:
            poster_url = ""
            if m.preview_image:
                poster_url = request.build_absolute_uri(m.preview_image.url)
            models_list.append({
                "id": str(m.id),
                "name": m.title or (m.product.name if m.product else "3D Model"),
                "url": request.build_absolute_uri(m.file.url),
                "poster": poster_url,
            })

        default_model_id = cfg.get("defaultModelId", models_list[0]["id"] if models_list else "")

        contact = cfg.get("contact", {
            "address": site.address or "تهران، خیابان ولیعصر، پلاک ۱۰",
            "phone": site.contact_phone or "021-00000000",
            "email": site.contact_email or "info@newmoonhome.ir",
        })

        theme = cfg.get("theme", {
            "defaultMode": "dark",
            "allowUserToggle": True,
        })

        data = {
            "brand": brand,
            "hero": hero,
            "nav": nav,
            "categories": categories,
            "products": products_list,
            "models": models_list,
            "defaultModelId": default_model_id,
            "contact": contact,
            "theme": theme,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        site, _ = SiteSetting.objects.get_or_create(site_name="NEWMOON HOME")
        payload = request.data or {}
        site.lovable_config = payload

        if "brand" in payload and isinstance(payload["brand"], dict):
            if payload["brand"].get("name"):
                site.site_name = payload["brand"]["name"]
            if payload["brand"].get("tagline"):
                site.site_description = payload["brand"]["tagline"]
        if "contact" in payload and isinstance(payload["contact"], dict):
            if payload["contact"].get("phone"):
                site.contact_phone = payload["contact"]["phone"]
            if payload["contact"].get("email"):
                site.contact_email = payload["contact"]["email"]
            if payload["contact"].get("address"):
                site.address = payload["contact"]["address"]

        site.save()
        return Response(payload, status=status.HTTP_200_OK)


class Model3DUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file") or request.FILES.get("model")
        if not file_obj:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        title = request.POST.get("name", file_obj.name)
        obj = ProductThreeD.objects.create(
            title=title, file=file_obj, file_format=file_obj.name.split(".")[-1].lower()
        )

        poster_url = ""
        if obj.preview_image:
            poster_url = request.build_absolute_uri(obj.preview_image.url)

        return Response(
            {
                "id": str(obj.id),
                "name": obj.title,
                "url": request.build_absolute_uri(obj.file.url),
                "poster": poster_url,
            },
            status=status.HTTP_201_CREATED,
        )
