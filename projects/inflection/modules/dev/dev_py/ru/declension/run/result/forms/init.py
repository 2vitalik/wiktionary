from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.forms.init'  # local


@a.call(module)
def init_forms(i):  # export  # Генерация словоформ
    r = i.result  # local
    p = i.parts  # local

    if i.calc_sg:
        r['nom-sg'] = p.stems['nom-sg'] + p.endings['nom-sg']
        r['gen-sg'] = p.stems['gen-sg'] + p.endings['gen-sg']
        r['dat-sg'] = p.stems['dat-sg'] + p.endings['dat-sg']
        r['acc-sg'] = ''
        r['ins-sg'] = p.stems['ins-sg'] + p.endings['ins-sg']
        r['prp-sg'] = p.stems['prp-sg'] + p.endings['prp-sg']
    # end

    if i.calc_pl:
        r['nom-pl'] = p.stems['nom-pl'] + p.endings['nom-pl']
        r['gen-pl'] = p.stems['gen-pl'] + p.endings['gen-pl']
        r['dat-pl'] = p.stems['dat-pl'] + p.endings['dat-pl']
        r['acc-pl'] = ''
        r['ins-pl'] = p.stems['ins-pl'] + p.endings['ins-pl']
        r['prp-pl'] = p.stems['prp-pl'] + p.endings['prp-pl']
    # end
# end


@a.starts(module)
def init_srt_forms(func, i):  # export  # todo move to `init_forms` (with if i.adj) ?
    p = i.parts  # local
    r = i.result  # local

    if i.calc_sg:
        r['srt-sg'] = p.stems['srt-sg'] + p.endings['srt-sg']
    # end
    if i.calc_pl:
        r['srt-pl'] = p.stems['srt-pl'] + p.endings['srt-pl']
    # end
    _.ends(module, func)
# end


# return export
