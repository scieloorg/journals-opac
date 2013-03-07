#
#   DEVE SER MANTIDA A ORDEM DOS ARQUIVOS JS e CSS
#

from django_assets import Bundle, register

base_bundle = Bundle('../static/js/jquery-1.9.1.js')

app_bundle = Bundle('../static/js/languages.js',
                    '../static/js/ratchet.js',
                    '../static/js/bootstrap.js',
                    '../static/js/google_jsapi.js')

js = Bundle(base_bundle, app_bundle, filters='yui_js', output='bundle.min.js')

register('js', js)

css = Bundle('../static/css/bootstrap.css',
             '../static/css/style.css',
             filters='yui_css',
             output='bundle.min.css')

register('css', css)
