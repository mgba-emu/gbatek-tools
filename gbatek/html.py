from bs4 import BeautifulSoup, Comment

class GBATekHTML(object):
    def __init__(self):
        super(GBATekHTML, self).__init__()
        self.sections = {}
        self.crosslinks = []

    def load(self, f):
        self.html = BeautifulSoup(f, from_encoding='latin-1')
        self.output = True
        self.markdown = ''.join(self.parse(self.html.body))

    def format_line(self, text):
        text = text.replace('\r', '')
        text = text.replace('*', '\*')
        text = text.replace('_', '\_')
        text = text.replace('<', '\<')
        return text + '\n'

    def enable_section(self, section, enable):
        self.sections[section] = enable

    def crosslink(self, anchor, page):
        self.crosslinks.append((anchor, page))

    def parse(self, elem, depth=0):
        markdown = []
        if not elem.name:
            if type(elem) == Comment:
                # Is there seriously not a better way to do this??
                return []
            markdown.extend([self.format_line(line) for line in elem.string.split('\n') if line.strip()])
        else:
            contents = []
            if len(elem.contents):
                for child in elem.children:
                    contents.extend(self.parse(child, depth + 1))
            elif elem.string and elem.string.strip():
                contents = [self.format_line(line) for line in elem.string.split('\n')]

            if elem.name == 'a':
                if 'href' in elem.attrs:
                    if elem.parent.name == 'body':
                        markdown.append('- ')
                    href = elem['href']
                    if href[0] == '#':
                        for xref, url in self.crosslinks:
                            if href[1:].startswith(xref):
                                href = url + href
                                break
                    markdown.append('[%s](%s)' % (''.join(contents).strip(), href))
                else:
                    markdown.append(str(elem))
            elif elem.name == 'b':
                markdown.append('\n## ' + ''.join(contents).strip() + '\n\n')
            elif elem.name == 'pre':
                if '_' in contents[0] or '  ' in contents[0]:
                    strings = []
                    for child in elem.children:
                        if child.name and child.name == 'b':
                            strings.append(str(child.contents[0]))
                        else:
                            strings.append(str(child))
                    markdown.append('```' + ''.join(strings) + '```\n')
                else:
                    markdown.extend(contents)
                markdown.append('\n')
            elif elem.name == 'font' and 'size' in elem.attrs:
                size = 3 - int(elem['size'])
                if size > 0:
                    if size == 1:
                        self.output = self.sections.get(contents[-1].strip().split()[0], True)
                    markdown.append('\n%s %s\n\n' % ('#' * size, ''.join([content.strip() for content in contents])))
            elif elem.name == 'br':
                markdown.append('\n')
            elif elem.name == 'table':
                for line in contents:
                    if not line.strip():
                        continue
                    if line.startswith('\n') or line.startswith('```'):
                        markdown.append(line)
                    else:
                        leading_spaces = len(line) - len(line.lstrip(' '))
                        if leading_spaces > 1:
                            markdown.append(' ' * (2 * (leading_spaces - 1)))
                        markdown.append('- ' + line.strip() + '\n')
                markdown.append('\n')
            else:
                markdown.extend(contents)
        if depth != 1 or self.output:
            return markdown
        else:
            return []
