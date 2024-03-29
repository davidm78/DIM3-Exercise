# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from tg.models import Category, Page
from django.shortcuts import render_to_response


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


def add_category(request):
        # immediately get the context - as it may contain posting data
        context = RequestContext(request)
        if request.method == 'POST':
                # data has been entered into the form via Post
                form = CategoryForm(request.POST)
                if form.is_valid():
                        # the form has been correctly filled in,
                        # so lets save the data to the model
                        cat = form.save(commit=True)
                        # show the index page with the list of categories
                        return index(request)
                else:
                        # the form contains errors,
                        # show the form again, with error messages
                        pass
        else:
                # a GET request was made, so we simply show a blank/empty form.
                form = CategoryForm()

        # pass on the context, and the form data.
        return render_to_response('rango/add_category.html',
                {'form': form }, context)

