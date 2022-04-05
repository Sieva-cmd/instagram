from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
from .models import Comments


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CommentForm(forms.ModelForm):
    # comment = forms.CharField(label='Leave a comment',max_length=30)
    comment = forms.CharField(widget=EmojiPickerTextareaAdmin)

    class Meta:
        model = Comments
        fields = ('comment',)
