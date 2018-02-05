from bs4 import BeautifulSoup, Comment

class GBATekHTML(object):
    def load(self, f):
        self.html = BeautifulSoup(f, from_encoding='latin-1')
        self.markdown = ''.join(self.parse(self.html.body))
        print(self.markdown)

    def format_line(self, text):
        text = text.replace('\r', '')
        text = text.replace('*', '\*')
        text = text.replace('_', '\_')
        text = text.replace('<', '\<')
        return text + '\n'

    def parse(self, elem):
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
                    contents.extend(self.parse(child))
            elif elem.string and elem.string.strip():
                contents = [self.format_line(line) for line in elem.string.split('\n')]

            if elem.name == 'a':
                if 'href' in elem.attrs:
                    if elem.parent.name == 'body':
                        markdown.append('- ')
                    markdown.append('[%s](%s)' % (''.join(contents).strip(), elem['href']))
                else:
                    markdown.append(str(elem))
            elif elem.name == 'b':
                markdown.append('\n### ' + ''.join(contents).strip() + '\n\n')
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
            elif elem.name == 'font':
                size = 4 - int(elem['size'])
                markdown.append('\n%s %s\n\n' % ('#' * size, ''.join(contents).strip()))
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
        return markdown
