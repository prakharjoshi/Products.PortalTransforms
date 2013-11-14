### Register Transforms
### This is interesting because we don't expect all transforms to be
### available on all platforms. To do this we allow things to fail at
### two levels
### 1) Imports
###    If the import fails the module is removed from the list and
###    will not be processed/registered
### 2) Registration
###    A second phase happens when the loaded modules register method
###    is called and this produces an instance that will be used to
###    implement the transform, if register needs to fail for now it
###    should raise an ImportError as well (dumb, I know)

from logging import DEBUG, ERROR
from Products.PortalTransforms.utils import log
from Products.PortalTransforms.libtransforms.utils import MissingBinary
modules = [
    'st',             # zopish
    'rest',           # docutils
    'word_to_html',   # uno, com, wvware
    'safe_html',      # extract <body> and remove potentially harmful tags
    'html_body',      # extract only the contents of the <body> tag
    'html_to_text',   # re based transform
    'text_to_html',   # wrap text in a verbatim env
    'text_pre_to_html',   # wrap text into a pre
    'pdf_to_html',    # sf.net/projects/pdftohtml
    'pdf_to_text',    # www.foolabs.com/xpdf
    'rtf_to_html',    # sf.net/projects/rtf-converter
    'rtf_to_xml',     # sf.net/projects/rtf2xml
    'image_to_png',   # transforms any image to a PNG image
    'image_to_gif',   # transforms any image to a GIF image
    'image_to_jpeg',  # transforms any image to a JPEG image
    'image_to_pcx',   # transforms any image to a PCX image
    'image_to_ppm',   # transforms any image to a PPM image
    'image_to_tiff',  # transforms any image to a TIFF image
    'image_to_bmp',   # transforms any image to a BMP image
    'lynx_dump',      # lynx -dump
    'python',         # python source files, no dependancies
    'identity',       # identity transform, no dependancies
    'markdown_to_html',  # markdown, depends python-markdown
    'textile_to_html',  # textile, depends on PyTextile
    'web_intelligent_plain_text_to_html',
    'html_to_web_intelligent_plain_text',
    ]

g = globals()
transforms = []
for m in modules:
    try:
        ns = __import__(m, g, g, None)
        transforms.append(ns.register())
    except ImportError, e:
        msg = "Problem importing module %s : %s" % (m, e)
        log(msg, severity=ERROR)
    except MissingBinary, e:
        log(str(e), severity=DEBUG)
    except Exception, e:
        import traceback
        traceback.print_exc()
        log("Raised error %s for %s" % (e, m), severity=ERROR)


def initialize(engine):
    for transform in transforms:
        engine.registerTransform(transform)
