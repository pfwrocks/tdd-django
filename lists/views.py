from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
	return render(request, 'home.html')

def view_list(request, list_id):
	lst = List.objects.get(id=list_id)
	error = None
	if request.method == 'POST':
		try:
			item = Item(text=request.POST['item_text'], list=lst)
			item.full_clean()
			item.save()
			return redirect(f'/lists/{list_id}/')
		except ValidationError:
			error = "You can't have an empty list item"
	return render(request, 'list.html', {'list': lst, 'error': error})

def new_list(request):
	lst = List.objects.create()
	item = Item.objects.create(text=request.POST['item_text'], list=lst)
	try:
		item.full_clean()
	except ValidationError:
		lst.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {'error': error})
	return redirect(f'/lists/{lst.id}/')
