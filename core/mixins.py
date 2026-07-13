class SeoContextMixin:
    """افزودن متا تگ‌های پویا به context تمپلیت."""

    seo_title = ''
    seo_description = ''

    def get_seo_title(self):
        return self.seo_title

    def get_seo_description(self):
        return self.seo_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_title'] = self.get_seo_title()
        context['seo_description'] = self.get_seo_description()
        return context
