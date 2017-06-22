#!/usr/bin/python3

import string
import re
import shlex
from pyparsing import ZeroOrMore, Regex

def substr(str1, start="", end=""):
    p1 = str1.find(start)
    if p1 >= 0:
        str2 = str1[p1 + len(start):]
    else:
        str2 = str1
    p2 = str2.find(end)
    if end != "" and p2 >= 0:
        return str2[0:p2]
    else:
        return str2

def split_quote(s):
    r_link_ref = Regex(r'\[[^]]*\]:.*') # match [1]:http:....
    r_link_text = Regex(r'(\[[^]]*\])+') # match [text][1]
    r_link_url = Regex(r'\[[^]]*\]\(.*\)') # match [text](http://)
    r_code_section = Regex(r'```')
    r_code_html = Regex(r'<[^>]*>')
    r_quote_1 = Regex(r'\'[^\']*\'') # not split '....'
    r_quote_2 = Regex(r'"[^"]*"')
    r_quote_code = Regex(r'\`[^`]*\`')
    r_word = Regex(r'[^ ]+')
    parser = ZeroOrMore( r_link_ref | r_link_url | r_link_text | r_code_section | r_code_html | r_quote_1 | r_quote_2 | r_quote_code | r_word)
    return parser.parseString(s)

def is_num_list(word):
    pattern = re.compile('\d+\.')
    return pattern.match(word)

def is_code_inline(word):
    pattern = re.compile('`[^`]+`')
    return pattern.match(word)

def is_link_text(word):
    pattern = re.compile('(\[[^]]*\])+')
    return pattern.match(word)

def is_link_url(word):
    pattern = re.compile('\[[^]]*\]\(.*\)')
    return pattern.match(word)

def is_url_comment(word):
    pattern = re.compile('\[[^]]*\]:.*')
    return pattern.match(word)

class Markdown():

    def __init__(self):
        self.code_mode = False
        self.code2_mode = False
        self.p_mode = False
        self.list_mode = False
        self.list_deep = 0
        self.nlist_mode = False
        self.quote_mode = False
        self.urls = {}

    def __convert_line(self, line):
        words = split_quote(line.strip())
        ret = ''
        for w in words:
            # print(w)
            if w.startswith('**') and w.endswith('**'):
                ret += '<strong>%s</strong> ' % w[2:-2]
            elif w.startswith('__') and w.endswith('__'):
                ret += '<strong>%s</strong> ' % w[2:-2]
            elif w.startswith('*') and w.endswith('*'):
                ret += '<em>%s</em> ' % w[1:-1]
            elif w.startswith('_') and w.endswith('_'):
                ret += '<em>%s</em> ' % w[1:-1]
            elif is_code_inline(w):
                ret += '<code>%s</code> ' % w[1:-1]
            elif is_link_url(w):
                # print(w)
                try:
                    text = substr(w, '[', ']')
                    url = substr(w, '(', ')')
                    ret += '<a href=%s>%s</a> ' % (url, text)
                except Exception as e:
                    ret += '<a href=%s>%s</a> ' % ('#', text)
            elif is_link_text(w):
                p = re.compile('\[[^]]*\]')
                a = p.findall(w)
                # print(w, a)
                if len(a) == 2:
                    prompt = a[0][1:-1]
                    urlkey = a[1][1:-1]
                    try:
                        ret += '<a href=%s>%s</a> ' % (self.urls[urlkey], prompt)
                    except Exception as e:
                        ret += '<a href=%s>%s</a> ' % ('#', prompt)
                else:
                    ret += w
            elif line.count('`') >= 2 and w.startswith('`') and not w.endswith('`'):
                self.code_mode = True
                ret += '<code>%s ' % w[1:]
            elif self.code_mode and w.endswith('`'):
                ret += '%s</code> ' % w[:-1]
                self.code_mode = False
            else:
                ret += w + ' '
        return ret.strip()

    def __convert_header(self, level, line):
        line = line[line.find(' '):]
        return '<h%d>%s</h%d>' % (level, self.__convert_line(line), level)

    def __convert_list(self, line):
        line = line[line.find(' '):]
        return '<li>%s</li>' % (self.__convert_line(line))

    def __collect_url(self, lines):
        pattern = re.compile('\[.+\]\:')
        for l in lines.split('\n'):
            # [keyword]:
            if pattern.match(l):
                k = substr(l, '[', ']')
                v = l[l.find(':') + 1:]
                self.urls[k] = v.strip()
        # print(self.urls)
        pass

    def convert(self, lines):
        self.__collect_url(lines)

        out = ''
        for l in lines.split('\n'):
            words = split_quote(l)
            if len(words) == 0:
                if self.p_mode:
                    self.p_mode = False
                    out += '</p>\n'
                if self.list_mode:
                    self.list_mode = False
                    out += '</ul>\n'
                if self.nlist_mode:
                    self.nlist_mode = False
                    out += '</ol>\n'
                if self.quote_mode:
                    self.quote_mode = False
                    out += '</blockquote>\n'
                out += '\n'
                continue
            # print(words)
            if self.code2_mode:
                if words[0] == '```':
                    out += '</code></pre>\n'
                    self.code2_mode = False
                    out += '\n'
                else:
                    out += l + '\n'
                continue
            else:
                if words[0] == '```':
                    out += '<pre><code>\n'
                    self.code2_mode = True
                    continue

            if self.quote_mode:
                if words[0] != '>':
                    out += '</blockquote>\n'
                    self.quote_mode = False
            else:
                if words[0] == '>':
                    out += '<blockquote>\n'
                    self.quote_mode = True
            if self.quote_mode:
                if len(words) > 1:
                    out += l[l.find('>') + 1:] + '<br>'
                else:
                    out += '<br>'
                continue

            if words[0] == '#':
                out += self.__convert_header(1, l)
            elif words[0] == '##':
                out += self.__convert_header(2, l)
            elif words[0] == '###':
                out += self.__convert_header(3, l)
            elif words[0] == '####':
                out += self.__convert_header(4, l)
            elif words[0] == '#####':
                out += self.__convert_header(5, l)
            elif words[0] == '######':
                out += self.__convert_header(6, l)
            elif words[0] == '#######':
                out += self.__convert_header(7, l)
            elif words[0] in ['-', '+', '*']:
                if not self.list_mode:
                    self.list_mode = True
                    out += '<ul>\n'
                out += self.__convert_list(l)
            elif is_num_list(words[0]):
                if not self.nlist_mode:
                    self.nlist_mode = True
                    self.nlist_index = 0
                    out += '<ol>\n'
                out += self.__convert_list(l)
            elif is_url_comment(words[0]):
                pass
            else:
                if not self.p_mode:
                    self.p_mode = True
                    out += '<p>\n'
                out += self.__convert_line(l)
            out += '\n'
        # mode end
        if self.list_mode:
            self.list_mode = False
            out += '</ul>\n'
        if self.nlist_mode:
            self.nlist_mode = False
            out += '</ol>\n'
        if self.quote_mode:
            self.quote_mode = False
            out += '</blockquote>\n'
        if self.code2_mode:
            self.code2_mode = False
            out += '<pre><code>\n'
        if self.p_mode:
            self.p_mode = False
            out += '</p>\n'
        out += '\n'
        return out


def convert_markdown(s):
    print('-----------other-------------')
    markdowner = markdown2.Markdown()
    s = markdowner.convert(s)
    # fixup
    # s = s.replace('<p><code>', '<pre><code>')
    # s = s.replace('</code></p>', '</code></pre>')
    return s


def convert_test(s):
    print('----------- my  -------------')
    markdowner = Markdown()
    s = markdowner.convert(s)
    return s



if __name__ == '__main__':
    print('start')

    t1 = '# Header **1** bold\n\n## header _2_ italic\n\n### header 3 `code` word'
    print(convert_markdown(t1))
    print(convert_test(t1))

    t1 = 'line **1** bold\nline _2_ italic\n\nline 3 `code` word'
    print(convert_markdown(t1))
    print(convert_test(t1))

    t1 = '- list1\n+ list2\n\nline 3 `code` word'
    print(convert_markdown(t1))
    print(convert_test(t1))

    t1 = '```\n+ list2\n\n> line 3 `code` word\n```\n'
    print(convert_markdown(t1))
    print(convert_test(t1))

    t1 = '> + list2\n>\n> line \n3 `code` word\n```\n'
    print(convert_markdown(t1))
    print(convert_test(t1))

    t1 = '1. list2\n2. line \n3. `code` word\n```\n'
    print(convert_markdown(t1))
    print(convert_test(t1))

    t1 = 'this is "hello world" \'test ddd\' `com add` <font color=red>nihao [a a a][1] [basd sd] [cd dd ]</font>\n```\nhello\nasdasd```\n'  
    s = shlex.shlex(t1)
    print(list(s))
    parser = ZeroOrMore(Regex(r'(\[[^]]*\])+') | Regex(r'```') | Regex(r'<[^>]*>') | Regex(r'\[[^]]*\]') | Regex(r'\'[^"]*\'') | Regex(r'"[^"]*"') | Regex(r'\`[^`]*\`') | Regex(r'[^ ]+'))
    for i in parser.parseString(t1): 
        print(i)

    t1 = '[Bug 412968][1] 1162: device level allow to save'
    print(is_link_text(t1))
    p = re.compile('\[[^]]*\]')
    a = p.findall(t1)[1]
    # b = p.match(t1).group(1)
    print(a)
