from django import forms

class AnimeSearch(forms.Form):
	search_query = forms.CharField()