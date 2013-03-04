# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from tg.models import Category, Page



def index(request):
        template = loader.get_template('tg/index.html')

        # Request all the categories.
        cat_list = Category.objects.all()
	for cat in cat_list:
    		category_name = cat.name
    		cat.url = encode_category(category_name)
        # Put the data into the context
        context = RequestContext(request,{ 'cat_list': cat_list })

        return HttpResponse(template.render(context))

def category(request, category_name_url):
        template = loader.get_template('tg/category.html')

        category_name = decode_category(category_name_url)
        context_dict = {'category_name_url': category_name_url,
                                'category_name': category_name}
        # Select the Category object given its name.
        # In models, we defined name to be unique,
        # so there so only be one, if one exists.
        cat = Category.objects.filter(name=category_name)
        if cat:
                # selects all the pages associated with the selected category
                pages = Page.objects.filter(category=cat)
                context_dict['pages'] = pages

        context = RequestContext(request, context_dict)
        return HttpResponse(template.render(context))

def encode_category(category_name):
        # returns the name converted for insert into url
        return category_name.replace(' ','_')

def decode_category(category_url):
        # returns the category name given the category url portion
        return category_url.replace('_',' ')
