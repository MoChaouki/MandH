from .models import Category

def categories(request):
    # Retrieve categories from the database
    categories = Category.objects.all()
    # Return a dictionary with the categories
    return {'categories': categories}


