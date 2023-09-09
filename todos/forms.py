from pyexpat import model
from django import forms
from todos.models import Todo


class create_task_form(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ['title', 'description', 'priority']


class task_update_form(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ['title', 'description', 'priority']
    
    def save(self, commit=True):
        todo = self.instance
        todo.title = self.cleaned_data['title']
        todo.description = self.cleaned_data['description']
        todo.priority = self.cleaned_data['priority']

        if commit:
            todo.save()
        return todo

