from django import forms
from .models import Memo, Section, Chapter, Task, TaskUpdate


class CommentForm(forms.Form):
    name = forms.CharField(label='称呼', max_length=16, error_messages={
        'required': '请填写您的称呼',
        'max_length': '称呼太长'
    })

    email = forms.EmailField(label='邮箱', error_messages={
        'required': '请填写您的邮箱',
        'invalid': '邮箱格式不正确'
    })

    content = forms.CharField(label='评论内容', error_messages={
        'required': '请填写您的评论内容',
        'max_length': '评论内容太长'
    })


class MemoForm(forms.ModelForm):

    class Meta:
        model = Memo
        fields = '__all__'


class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'

    def bind_memo(self, memo_id):
        try:
            self.fields['memo'].queryset = Memo.objects.filter(id=memo_id)
            if len(self.fields['memo'].queryset) > 0:
                self.fields['memo'].initial = self.fields['memo'].queryset[0]
            self.fields['chapter'].queryset = Chapter.objects.filter(memo=memo_id)
            if len(self.fields['chapter'].queryset) > 0:
                n = len(self.fields['chapter'].queryset)
                self.fields['chapter'].initial = self.fields['chapter'].queryset[n-1]
            self.fields['type'].initial = self.fields['type'].queryset[0]
        except Exception as err:
            pass


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = '__all__'

    def bind_memo(self, memo_id):
        self.fields['memo'].queryset = Memo.objects.filter(id=memo_id)
        self.fields['memo'].initial = self.fields['memo'].queryset[0]
        self.fields['title'].initial = '%d) ' % (len(Chapter.objects.filter(memo=memo_id)) + 1)


class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = TaskUpdate
        fields = '__all__'

    def bind_task(self, task_id):
        self.fields['task'].queryset = Task.objects.filter(id=task_id)
        self.fields['task'].initial = self.fields['task'].queryset[0]
