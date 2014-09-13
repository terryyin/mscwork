c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
c.NbConvertApp.notebooks = ['LifecycleTools.ipynb']
c.NbConvertApp.export_format = 'latex'
c.NbConvertApp.postprocessor_class = 'PDF'

c.Exporter.template_file = 'citations'

import re
def cite_with_pages(s):
    return re.sub(r"(\\cite)\{(\[.*?\])", r"\1\2{", s, flags=re.DOTALL)

get_config().Exporter.filters = {
    "cite_with_pages": cite_with_pages}
