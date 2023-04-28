from django import forms
from blog.models import Comment, Post, Category
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_select2.forms import Select2Widget
from taggit.forms import TagField

class EmailPostForm(forms.Form):

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
class NewPostForm(forms.ModelForm):
    
    title = forms.CharField(label=_('Название поста'))
    body = forms.CharField(label=_('Текст:'), widget=forms.Textarea)
    image = forms.ImageField(label=_('Картинка (если нужно)'), widget=forms.ClearableFileInput, required=False)
    category = forms.ModelChoiceField(label=_('Категория (блог)'), queryset=Category.objects.none())
    slug = forms.SlugField(label=_('Имя в адресной строке'), required=False)
    tags = TagField(label=_('Теги'))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем текущего пользователя из kwargs
        super(NewPostForm, self).__init__(*args, **kwargs)
        if user:
            # Ограничиваем queryset для поля category только категориями, принадлежащими текущему пользователю
            self.fields['category'].queryset = Category.objects.filter(author=user)
    
    class Meta:
        model = Post
        fields = ['title', 'tags', 'slug', 'body', 'image', 'category', 'status']
        
    def clean_slug(self):
        
        slug = self.cleaned_data.get('slug')
        
        if not slug:
            
            title = self.cleaned_data.get('title')
            slug = slugify(title)
            
        return slug
    
class NewCategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ('name',)
        
class EditPostForm(forms.ModelForm):
    
    title = forms.CharField(label=_('Название поста'))
    body = forms.CharField(label=_('Текст:'), widget=forms.Textarea)
    image = forms.ImageField(label=_('Картинка (если нужно)'), widget=forms.ClearableFileInput, required=False)
    category = forms.ModelChoiceField(label=_('Категория (блог)'), queryset=Category.objects.none())
    slug = forms.SlugField(label=_('Имя в адресной строке'), required=False)
    tags = TagField(label=_('Теги'))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем текущего пользователя из kwargs
        super(EditPostForm, self).__init__(*args, **kwargs)
        
        self.fields['category'] = forms.ModelChoiceField(
            label=_('Категория (блог)'),  
            queryset=Category.objects.filter(author=user)
            )
    
    class Meta:
        model = Post
        fields = ['title', 'tags', 'slug', 'body', 'image', 'category', 'status']
    
class CommentForm(forms.ModelForm):

    class Meta():

        model = Comment
        fields = ('name', 'email', 'body')