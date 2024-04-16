from django.views.generic import ListView, DetailView


class ListViewBreadCrumbMixin(ListView):
    breadcrumbs = {"Головна": "/",}
    
    def get_breadcrumb(self): # метод для формування хлібних крихт
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):# метод для передачі хлібних крихт в контекст
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumb()
        return context
    
    
class DetailViewBreadCrumbMixin(DetailView):
    breadcrumbs = {"Головна": "/",}
    
    def get_breadcrumb(self): # метод для формування хлібних крихт
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):# метод для передачі хлібних крихт в контекст
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumb()
        return context