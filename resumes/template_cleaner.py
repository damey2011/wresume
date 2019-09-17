from bs4 import BeautifulSoup


def replace_statics():
    template_path = input('Enter Template Path: ')
    prefix_replace = input('Enter Prefix to Remove: ')
    static_folder = input('Enter the folder where static files are contained: ')
    static_cat = input('Should categorize static: ')
    """
        /Users/oluwanifemi/PycharmProjects/wresume/templates/stock/paiva/index.html
        ./Marcelo Paiva - Product Designer and Educator_files/
        blog-assets/material
    """

    with open(template_path, 'r+') as file:
        file.seek(0)
        content = file.read()
        content = '{% load static general_tags %} \n' + content
        bs = BeautifulSoup(content, 'html.parser')
        css_tags = bs.find_all('link', {'rel': 'stylesheet'})
        script_tags = bs.find_all('script')
        img_tags = bs.find_all('img')
        loom_container = bs.find_all('loom-container')
        mfa = bs.find_all('div', {'id': 'mfa_inject'})
        mfas = bs.find_all('div', {'id': 'mfa_inject_cartdata'})

        for mf in mfa:
            mf.decompose()

        for mf in mfas:
            mf.decompose()

        for c in loom_container:
            c.decompose()

        for css in css_tags:
            href = css['href'].replace(prefix_replace, '')
            if '//' not in href:
                if static_cat:
                    css['href'] = "{% static '" + static_folder + "/css/" + href + "' %}"
                else:
                    css['href'] = "{% static '" + static_folder + href + "' %}"

        for script in script_tags:
            if script.get('src'):
                if script.get('src').startswith('chrome-extension') or 'analytics.js' in script.get('src'):
                    script.decompose()
                else:
                    src = script['src'].replace(prefix_replace, '')
                    if '//' not in src:
                        if static_cat:
                            script['src'] = "{% static '" + static_folder + "/js/" + src + "' %}"
                        else:
                            script['src'] = "{% static '" + static_folder + src + "' %}"

        for img in img_tags:
            src = img['src'].replace(prefix_replace, '')
            if '//' not in src:
                if static_cat:
                    img['src'] = "{% static '" + static_folder + "/img/" + src + "' %}"
                else:
                    img['src'] = "{% static '" + static_folder + src + "' %}"

        file.truncate(0)
        file.write(bs.prettify())


replace_statics()
