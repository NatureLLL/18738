#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 22:16:48 2018

@author: nature
"""

from django import forms

from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

from grumblr.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=42)
    firstname = forms.CharField(max_length=42)
    lastname = forms.CharField(max_length=42)
    email = forms.EmailField()
    password1 = forms.CharField(max_length = 200, label='Password',widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, label='Confirm password',widget = forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
    
     # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username
        
class PasswordForm(forms.Form):
    old_password = forms.CharField(max_length = 200, label='Old password',widget = forms.PasswordInput())
    new_password1 = forms.CharField(max_length = 200, label='New password',widget = forms.PasswordInput())
    new_password2 = forms.CharField(max_length = 200, label='Confirm new password',widget = forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
    
    
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    class Meta:
        model = Profile
        exclude = ('user', 'followers',)
        widgets = {
                'avatar': forms.FileInput(),
                }
        fields = ('avatar', 'age', 'first_name', 'last_name', 'bio', )

    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(initial=self.instance.user.first_name)
        self.fields['last_name'] = forms.CharField(initial=self.instance.user.last_name)


    def save(self, commit=True):
        m = super(ProfileForm, self).save(commit=False)
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.save()
        return super(ProfileForm, self).save(commit=commit)
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols': 80, 'rows':50, }))

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'width': "100%", 'cols': 80, 'rows': 50, }))
    post_id = forms.IntegerField()

    