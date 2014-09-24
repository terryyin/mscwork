c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
c.NbConvertApp.notebooks = ['LifecycleTools.ipynb']
c.NbConvertApp.export_format = 'latex'
c.NbConvertApp.postprocessor_class = 'PDF'

c.Exporter.template_file = 'citations'

import re
from collections import defaultdict

def cite_with_pages(s):
    return re.sub(r"(\\cite)\{(\[.*?\])", r"\1\2{", s, flags=re.DOTALL)

def img_extension(s):
    def replace_img_with_latex(match):
        def get_value(name):
            m = re.search(name + r"=(" +
                          r"\"(?:\\.|[^\"])*\"" +
                          r"|\'(?:\\.|[^\'])*?\'" +
                          r"|[^\'\"].*?)[\s|\>]", match.group(0))
            if m:
                result = m.group(1)
                return result[1:-1] if result[0] in ('"', "'") else result
        values = defaultdict(str)
        width = get_value("width")
        if width:
            if width[-1] == "%":
                values["matrics"] = (r"[width=%.2f\textwidth]" %
                                     (float(width[:-1]) / 100))
        align = get_value("align")
        caption = get_value("alt")
        if align in ("left", "right"):
            lineheight = get_value("lineheight")
            if lineheight:
                values["lineheight"] = "[%s]" % lineheight
            values["align"] = ("\\begin{wrapfigure}%s{%s}{%.2f\\textwidth}\n" %
                               (values["lineheight"],
                                "LR"[align == "right"],
                                0.5 if width is None else
                                float(width[:-1]) * 1.05 / 100))
            values["endalign"] = "\n\\end{wrapfigure}"
        else:
            values["align"] = "\\begin{figure}[h]\n"
            values["endalign"] = "\n\\end{figure}"

        if caption:
            values["caption"] = "\n\\caption{%s}" % caption
        values["src"] = get_value("src")
        return ("{d[align]}\\centering\n\\includegraphics{d[matrics]}" +
                "{{{d[src]}}}{d[caption]}\n{d[endalign]}").format(d=values)
    return re.sub(r"\<\s*img.*?\>", replace_img_with_latex, s)


def dl_extension(s):
    s = re.sub(r"\<dl\>", r"\\begin{description}", s)
    s = re.sub(r"\</dl\>", r"\\end{description}", s)
    s = re.sub(r"\<dt\>(.*?)\</dt\>", r"\\item[\1] \\hfill \\\\", s)
    s = re.sub(r"\<dd\>(.*?)\</dd\>", r"\1", s, flags=re.DOTALL)
    return s

def ref_extension(s):
    s = re.sub(r"\<ref\>(.*?)\</ref\>", r"\\ref{\1}", s)
    return s


def markdown_extension(s):
    return ref_extension(dl_extension(img_extension(s)))

get_config().Exporter.filters = {
    "markdown_extension": markdown_extension,
    "cite_with_pages": cite_with_pages}
