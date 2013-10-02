let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Documents/communityvisweb
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 web/models.py
badd +833 web/views.py
badd +8 web/taxonomy_backend.py
badd +19 web/templates/index.html
badd +11 web/reference_import.py
badd +60 web/templates/taxonomy_detail.html
badd +49 web/templates/fragments/addReferenceModal.html
badd +1 viscommunityweb/urls.py
badd +1 viscommunityweb/settings.py
badd +196 web/templates/taxonomy.html
badd +7 web/taxonomy_cassandra.py
badd +63 web/reference_backend.py
badd +3 web/reference_cassandra.py
badd +6 web/cassandra_test.py
badd +22 web/admin.py
badd +46 web/reference_import_cassandra.py
badd +48 web/templates/reference.html
badd +29 web/templates/references_include.html
badd +1 web/reference_import
badd +45 web/ref_cass_test.py
badd +41 ref_cass_test.py
badd +1 web/templates/references.html
badd +13 taxonomy_init.py
badd +1 web/reference_couch.py
badd +74 web/reference_import_couch.py
badd +1 web/reference_import_c
badd +1 web/templates/reference
badd +623 web/static/css/style.css
badd +5 web/templates/base.html
badd +19 web/templates/taxonomy-header.html
badd +1 taxonomy/html
badd +86 web/templates/contact.html
badd +65 web/templates/volunteer.html
badd +20 web/templates/fragments/deleteReferenceModal.html
badd +41 web/templates/fragments/taxonomyModerationRequestModal.html
badd +27 web/templates/fragments/taxonomyRequestModal.html
badd +343 web/templates/profile.html
badd +1 web/templates/profile
badd +47 web/templates/fragments/RevokeModal.html
badd +12 web/templates/fragments/moveReferencesModal.html
badd +1 web/templates/taxonomy
badd +1 web/static/js/taxonomy_tree.js
badd +33 web/templates/taxonomy_edit_base.html
badd +2 web/templates/fragments/moveTaxonomyItemModal.html
badd +36 web/templates/fragments/splitModal.html
badd +22 web/templates/fragments/renameModal.html
badd +1 web/templates/fragments/delete
badd +15 web/templates/fragments/deleteModal.html
badd +19 web/templates/fragments/suggestionResponseModal.html
badd +40 web/templates/fragments/suggestModal.html
silent! argdel *
edit viscommunityweb/settings.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 46 - ((3 * winheight(0) + 49) / 98)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 030|
lcd ~/Documents/communityvisweb/viscommunityweb
tabedit ~/Documents/communityvisweb/web/templates/taxonomy.html
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 142 + 168) / 337)
exe '2resize ' . ((&lines * 54 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 194 + 168) / 337)
exe '3resize ' . ((&lines * 12 + 47) / 95)
exe 'vert 3resize ' . ((&columns * 194 + 168) / 337)
exe '4resize ' . ((&lines * 25 + 47) / 95)
exe 'vert 4resize ' . ((&columns * 194 + 168) / 337)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 191 - ((89 * winheight(0) + 46) / 93)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
191
normal! 0
lcd ~/Documents/communityvisweb/web/templates
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/fragments/moveReferencesModal.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 96 - ((24 * winheight(0) + 27) / 54)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
96
normal! 087|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/fragments/moveTaxonomyItemModal.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 4 - ((1 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 021|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/fragments/addReferenceModal.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 42 - ((7 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
42
normal! 030|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
exe 'vert 1resize ' . ((&columns * 142 + 168) / 337)
exe '2resize ' . ((&lines * 54 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 194 + 168) / 337)
exe '3resize ' . ((&lines * 12 + 47) / 95)
exe 'vert 3resize ' . ((&columns * 194 + 168) / 337)
exe '4resize ' . ((&lines * 25 + 47) / 95)
exe 'vert 4resize ' . ((&columns * 194 + 168) / 337)
tabedit ~/Documents/communityvisweb/web/views.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 161 + 168) / 337)
exe '2resize ' . ((&lines * 33 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 175 + 168) / 337)
exe '3resize ' . ((&lines * 29 + 47) / 95)
exe 'vert 3resize ' . ((&columns * 175 + 168) / 337)
exe '4resize ' . ((&lines * 29 + 47) / 95)
exe 'vert 4resize ' . ((&columns * 175 + 168) / 337)
argglobal
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 463 - ((48 * winheight(0) + 46) / 93)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
463
normal! 024|
lcd ~/Documents/communityvisweb/web
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/static/js/taxonomy_tree.js
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 210 - ((15 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
210
normal! 0
lcd ~/Documents/communityvisweb/web/static/js
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/taxonomy.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 96 - ((13 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
96
normal! 022|
lcd ~/Documents/communityvisweb/web/templates
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/fragments/deleteReferenceModal.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 3 - ((1 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 029|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
exe 'vert 1resize ' . ((&columns * 161 + 168) / 337)
exe '2resize ' . ((&lines * 33 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 175 + 168) / 337)
exe '3resize ' . ((&lines * 29 + 47) / 95)
exe 'vert 3resize ' . ((&columns * 175 + 168) / 337)
exe '4resize ' . ((&lines * 29 + 47) / 95)
exe 'vert 4resize ' . ((&columns * 175 + 168) / 337)
tabedit ~/Documents/communityvisweb/viscommunityweb/urls.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 26 - ((23 * winheight(0) + 46) / 93)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
26
normal! 082|
lcd ~/Documents/communityvisweb/viscommunityweb
tabedit ~/Documents/communityvisweb/web/views.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 46 + 47) / 95)
exe 'vert 1resize ' . ((&columns * 153 + 168) / 337)
exe '2resize ' . ((&lines * 46 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 153 + 168) / 337)
exe 'vert 3resize ' . ((&columns * 183 + 168) / 337)
argglobal
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 601 - ((22 * winheight(0) + 23) / 46)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
601
normal! 033|
lcd ~/Documents/communityvisweb/web
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/views.py
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 666 - ((33 * winheight(0) + 23) / 46)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
666
normal! 037|
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/models.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 122 - ((71 * winheight(0) + 46) / 93)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
122
normal! 037|
lcd ~/Documents/communityvisweb/web
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 46 + 47) / 95)
exe 'vert 1resize ' . ((&columns * 153 + 168) / 337)
exe '2resize ' . ((&lines * 46 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 153 + 168) / 337)
exe 'vert 3resize ' . ((&columns * 183 + 168) / 337)
tabedit ~/Documents/communityvisweb/web/reference_import_couch.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 92 + 47) / 95)
exe 'vert 1resize ' . ((&columns * 137 + 168) / 337)
exe '2resize ' . ((&lines * 92 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 215 + 168) / 337)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 75 - ((55 * winheight(0) + 46) / 92)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
75
normal! 025|
lcd ~/Documents/communityvisweb/web
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/models.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 143 - ((88 * winheight(0) + 46) / 92)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
143
normal! 063|
lcd ~/Documents/communityvisweb/web
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 92 + 47) / 95)
exe 'vert 1resize ' . ((&columns * 137 + 168) / 337)
exe '2resize ' . ((&lines * 92 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 215 + 168) / 337)
tabedit ~/Documents/communityvisweb/web/templates/base.html
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 71 + 47) / 95)
exe 'vert 1resize ' . ((&columns * 237 + 168) / 337)
exe '2resize ' . ((&lines * 61 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 115 + 168) / 337)
exe '3resize ' . ((&lines * 9 + 47) / 95)
exe 'vert 3resize ' . ((&columns * 115 + 168) / 337)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 5 - ((4 * winheight(0) + 35) / 71)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 038|
lcd ~/Documents/communityvisweb/web/templates
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/fragments/taxonomyRequestModal.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 46 - ((45 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 07|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
argglobal
edit ~/Documents/communityvisweb/web/templates/fragments/addReferenceModal.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 38 - ((4 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
38
normal! 017|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 71 + 47) / 95)
exe 'vert 1resize ' . ((&columns * 237 + 168) / 337)
exe '2resize ' . ((&lines * 61 + 47) / 95)
exe 'vert 2resize ' . ((&columns * 115 + 168) / 337)
exe '3resize ' . ((&lines * 9 + 47) / 95)
exe 'vert 3resize ' . ((&columns * 115 + 168) / 337)
tabedit ~/Documents/communityvisweb/web/reference_import_couch.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 74 - ((69 * winheight(0) + 49) / 98)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
74
normal! 045|
lcd ~/Documents/communityvisweb/web
2wincmd w
tabnext 5
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filmnrxoOtT
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
