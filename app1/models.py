from django.db import models

# Create your models here.


class Config(models.Model):
    bug_enable = models.BooleanField('Enable Bug List', default=False)
    task_enable = models.BooleanField('Enable Task List', default=False)
    note_enable  = models.BooleanField('Enable Note List', default=False)

class Category(models.Model):
    name = models.CharField('Text', max_length=16)

    def __str__(self):
        return '%s' % (self.name)


class Tag(models.Model):
    name = models.CharField('Text', max_length=16)

    def __str__(self):
        return '%s' % (self.name)


class SectionType(models.Model):
    name = models.CharField('Text', max_length=16)

    def __str__(self):
        return '%s' % (self.name)


class Blog(models.Model):
    title = models.CharField('Title', max_length=32)
    author = models.CharField('Author', max_length=16)
    content = models.TextField('Text')
    created = models.DateTimeField('Created', auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='Category')
    tags = models.ManyToManyField(Tag, verbose_name='Tag')


class Comment(models.Model):
    blog = models.ForeignKey(Blog, verbose_name='Blog')
    name = models.CharField('Name', max_length=16)
    email = models.EmailField('Email')
    content = models.CharField('Text', max_length=140)
    created = models.DateTimeField('Created', auto_now_add=True)


class Memo(models.Model):
    title = models.CharField('Title', max_length=128)
    author = models.CharField('Author', max_length=32)
    summary = models.TextField('Summary')
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Last modified', auto_now=True)
    category = models.ForeignKey(Category, verbose_name='Category')
    tag = models.ManyToManyField(Tag, verbose_name='Tag')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return 'MEMO%d - %s' % (self.id, self.title)


class Chapter(models.Model):
    memo = models.ForeignKey(Memo, verbose_name='Memo')
    title = models.CharField('Title', max_length=64)

    def __str__(self):
        return 'MEMO%d - %s' % (self.memo.id, self.title)


class Section(models.Model):
    memo = models.ForeignKey(Memo, verbose_name='Memo')
    chapter = models.ForeignKey(Chapter, verbose_name='Chapter')
    type = models.ForeignKey(SectionType, verbose_name='Type')
    keypoint = models.CharField('Key Point', blank=True, max_length=256)
    content = models.TextField('Text')
    modified = models.DateTimeField('Last modified', auto_now=True)

    def __str__(self):
        return '#%d %s %s %s' % (self.id, self.type, self.memo.title, self.chapter.title)

class Bug(models.Model):
    BUG_STATUS_CHOICES = (
            ('new', 'Assign'),
            ('wrk', 'Work-on'),
            ('rca', 'Root Cause'),
            ('sol', 'Solution'),
            ('qat', 'QA Test'),
            ('eco', 'ECO Submit'),
            ('fix', 'Fixed'),
            ('pen', 'Pending'),
        )
    bugno = models.CharField('Bug', max_length=16)
    desc = models.CharField('Description', max_length=256)
    comment = models.CharField('Comment', blank=True, max_length=256)
    status = models.CharField('Status', choices=BUG_STATUS_CHOICES, max_length=16)
    memo = models.ForeignKey(Memo, verbose_name='Memo')
    modified = models.DateTimeField('Last modified', auto_now=True)

    def __str__(self):
        return '#%s %s' % (self.bugno, self.desc)

class Task(models.Model):
    name = models.CharField('Name', max_length=256)
    started = models.DateField('Started')
    eta = models.DateField('ETA')
    bug = models.ForeignKey(Bug, verbose_name='Bug', blank=True, null=True)

    def __str__(self):
        return '#%s %s' % (self.id, self.name)

class TaskUpdate(models.Model):
    task = models.ForeignKey(Task, verbose_name='Task')
    complete = models.PositiveSmallIntegerField('complete')
    hours = models.PositiveSmallIntegerField('Hours')
    comment = models.CharField('Comment', max_length=256)
    updated = models.DateField('Updated', auto_now_add=True)

    def __str__(self):
        return '#%d %s +%d%% +%dh %s' % (self.task.id, self.task.name, self.complete, self.hours, self.comment)