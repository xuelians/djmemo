from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404

# Create your views here.

from .models import Memo, Comment, Category, Tag, Chapter, Section, Bug, Task, TaskUpdate
from .forms import CommentForm, MemoForm, SectionForm, ChapterForm, TaskUpdateForm
from .mkdown import Markdown
import datetime

DEBUG=1

def pdebug(*args, **kwargs):
    """print a debug message if debug level allows"""
    if DEBUG:
        print(*args, **kwargs)

def _convert_markdown(s):
    markdowner = Markdown()
    s = markdowner.convert(s)
    # fixup
    s = s.replace('<p><code>', '<pre><code>')
    s = s.replace('</code></p>', '</code></pre>')
    return s


def load_list():
    memos = Memo.objects.all().order_by('-modified')
    for m in memos:
        m.summary = _convert_markdown(m.summary)
    return memos


def _get_week_num(date=None):
    if date:
        d = datetime.date(date.year, date.month, date.day)
    else:
        d = datetime.date.today()
    _, n, _ = d.isocalendar()
    return int(n)

def _get_week_day(date=None):
    if date:
        d = datetime.date(date.year, date.month, date.day)
    else:
        d = datetime.date.today()
    _, _, day = d.isocalendar()
    return int(day)

def __load_task_subctx(task, week_date = True):
    updates = task.taskupdate_set.all()
    task.started_wk = 'wk%d.%d' % (_get_week_num(task.started), _get_week_day(task.started))
    task.eta_wk = 'wk%d.%d' % (_get_week_num(task.eta), _get_week_day(task.eta))
    task.complete = 0
    task.hours = 0
    task.week_hours = 0
    task.day_hours = [0, 0, 0, 0, 0]
    task.active = False
    task.updates = []
    this_week = _get_week_num()
    for up in updates:
        task.complete += up.complete
        task.hours += up.hours
        week = _get_week_num(up.updated)
        dow = _get_week_day(up.updated)
        if this_week == week:
            task.week_hours += up.hours
            task.day_hours[dow-1] += up.hours
        if week_date:
            datestr = 'wk%d.%d' % (week, dow)
        else:
            datestr = str(up.updated)
        task.updates.append('[%s] %s' % (datestr, up.comment))
    if task.complete < 100:
        task.day_left = (task.eta - datetime.date.today()).days
    task.comments = '\n'.join(task.updates)
    return task


def __load_task():
    year, nweek, dow = datetime.date.today().isocalendar()
    filted_tasks = []
    tasks = Task.objects.all()
    for t in tasks:
        t2 = __load_task_subctx(t)
        if t2.complete < 100 or t2.week_hours:
            filted_tasks.append(t2)  # not complete

    week_hours = 0
    day_hours = [0, 0, 0, 0, 0]
    for t in filted_tasks:
        week_hours += t.week_hours
        for i in range(5):
            day_hours[i] += t.day_hours[i]
    return {
        'year': year,
        'week': nweek,
        'dow': dow,
        'ntask': len(filted_tasks),
        'tasks': filted_tasks,
        'week_hours': week_hours,
        'day_hours': day_hours
    }


def get_list(request):
    try:
        config = Config.objects.all()[0]
    except:
        config = None
    ctx = {
        'config': config,
        'now': datetime.datetime.now(),
        'taskinfo': __load_task(),
        'bugs': Bug.objects.all().order_by('-modified'),
        'memos': load_list(),
        'form': MemoForm()
    }
    pdebug('render memo list')
    return render(request, 'memo_list.html', ctx)


def new_memo(request):
    pdebug('---> new_memo', request.method)
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save()
            memo.save()
            print('memo append')
        else:
            print('memo form invalid')
    pdebug('<--- new_memo')
    return HttpResponseRedirect(reverse('memo_get_list'))


def edit_summary(request, memo_id):
    try:
        memo = Memo.objects.get(id=memo_id)
    except Memo.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            memo = form.save()
            memo.save()
        return HttpResponseRedirect(reverse('memo_get_detail', args=[memo_id]))
    else:
        form = MemoForm(instance=memo)
        ctx = {
            'memo': memo,
            'form_memo': form
        }
        return render(request, 'memo_edit.html', ctx)


def load_detail(memo_id):
    try:
        memo = Memo.objects.get(id=memo_id)
    except Memo.DoesNotExist:
        raise Http404

    memo.summary = _convert_markdown(memo.summary)
    memo.chapter = memo.chapter_set.all()
    for c in memo.chapter:
        c.section = c.section_set.all()
        for s in c.section:
            s.keypoint = _convert_markdown(s.keypoint)
            s.content = _convert_markdown(s.content)
    return memo


def get_detail(request, memo_id):
    form_section = SectionForm()
    form_section.bind_memo(memo_id)
    form_chapter = ChapterForm()
    form_chapter.bind_memo(memo_id)
    ctx = {
        'memo': load_detail(memo_id),
        'form_section': form_section,
        'form_chapter': form_chapter
    }
    return render(request, 'memo_detail.html', ctx)


def add_section(request, memo_id):
    redir_url = reverse('memo_get_detail', args=[memo_id])
    print('redir_url=%s' % redir_url)
    if request.method == 'POST':
        form = SectionForm(request.POST)
        # print(form)
        if form.is_valid():
            section = form.save()
            section.save()
            # update time-stamp
            memo = Memo.objects.get(id=memo_id)
            memo.save()
            ctx = {
                'memo': load_detail(memo_id),
                'form_section': SectionForm(),
                'form_chapter': ChapterForm()
            }
            redir_arg = '#section_%s' % section.id if section.id > 0 else ''
            return HttpResponseRedirect(redir_url + redir_arg)
        else:
            print(form.errors)
            form_chapter = ChapterForm()
            form_chapter.bind_memo(memo_id)
            ctx = {
                'memo': load_detail(memo_id),
                'form_section': form,
                'form_chapter': form_chapter
            }
            return render(request, 'memo_detail.html', ctx)


def edit_section(request, memo_id, section_id=0):
    redir_url = reverse('memo_get_detail', args=[memo_id])
    print('redir_url=%s' % redir_url)
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save()
            section.save()
            # update time-stamp
            memo = Memo.objects.get(id=memo_id)
            memo.save()
        redir_arg = '#section_%s' % section.id if section.id > 0 else ''
        return HttpResponseRedirect(redir_url + redir_arg)
    else:
        form = SectionForm(instance=section)
        ctx = {
            'memo': load_detail(memo_id),
            'section': Section.objects.get(id=section_id),
            'form_section': form
        }
        return render(request, 'section_edit.html', ctx)


def add_chapter(request, memo_id):
    redir_url = reverse('memo_get_detail', args=[memo_id])
    print('redir_url=%s' % redir_url)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            # auto-index
            # n = len(Chapter.objects.filter(memo=memo_id))
            # chapter.title = '%d)' % (n+1) + chapter.title
            chapter = form.save()
            chapter.save()
            # update time-stamp
            memo = Memo.objects.get(id=memo_id)
            memo.save()
    ctx = {
        'memo': load_detail(memo_id),
        'form_section': SectionForm(),
        'form_chapter': ChapterForm()
    }
    return HttpResponseRedirect(redir_url)


def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST)
        if form.is_valid():
            memo = form.save()
            memo.save()
            return HttpResponseRedirect(reverse('memo_get_list'))
    else:
        form = TaskUpdateForm()
        form.bind_task(task_id)
        ctx = {
            'task': __load_task_subctx(task),
            'form': form
        }
    return render(request, 'task_update.html', ctx)


def export_task(request):
    taskinfo = __load_task()
    expstr = ''
    for t in taskinfo['tasks']:
        if t.week_hours > 0:
            if t.bug:
                task_title = '%s: %s' % (t.bug.bugno, t.name)
            else:
                task_title = t.name
            expstr += '| %d | %s | %s | %s | %d | %s | %s |\n' %\
                (t.id, task_title, t.started.strftime('%d %B %Y'), t.eta.strftime('%d %B %Y'), t.complete, t.week_hours, t.comments.replace('\n', '<br>'))
    return render(request, 'task_export.html', {'taskinfo':taskinfo, 'expstr': expstr})

# test


def index(request):
    return HttpResponse('Hello')


def home(request):
    s = 'this is django'
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    List = map(str, range(5))  # 一个长度为100的 List
    return render(request, 'home.html', {'string': s,
                                         'TutorialList': TutorialList,
                                         'info_dict': info_dict,
                                         'List': List})


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(reverse('add2', args=(a, b)))
