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
badd +0 web/models.py
badd +0 web/views.py
badd +8 web/taxonomy_backend.py
badd +50 web/templates/index.html
badd +11 web/reference_import.py
badd +60 web/templates/taxonomy_detail.html
badd +49 web/templates/fragments/addReferenceModal.html
badd +0 viscommunityweb/urls.py
badd +0 viscommunityweb/settings.py
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
badd +1 web/reference_import_couch.py
badd +0 web/reference_import_c
badd +1 web/templates/reference
badd +613 web/static/css/style.css
badd +70 web/templates/base.html
badd +19 web/templates/taxonomy-header.html
badd +1 taxonomy/html
badd +50 web/templates/contact.html
badd +65 web/templates/volunteer.html
badd +20 web/templates/fragments/deleteReferenceModal.html
badd +41 web/templates/fragments/taxonomyModerationRequestModal.html
badd +27 web/templates/fragments/taxonomyRequestModal.html
badd +343 web/templates/profile.html
badd +1 web/templates/profile
badd +47 web/templates/fragments/RevokeModal.html
badd +46 web/templates/fragments/moveReferencesModal.html
badd +1 web/templates/taxonomy
badd +0 web/static/js/taxonomy_tree.js
badd +33 web/templates/taxonomy_edit_base.html
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
let s:l = 46 - ((3 * winheight(0) + 46) / 93)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 030|
lcd ~/Documents/communityvisweb/viscommunityweb
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
exe 'vert 1resize ' . ((&columns * 133 + 173) / 346)
exe '2resize ' . ((&lines * 32 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 212 + 173) / 346)
exe '3resize ' . ((&lines * 28 + 48) / 97)
exe 'vert 3resize ' . ((&columns * 212 + 173) / 346)
exe '4resize ' . ((&lines * 33 + 48) / 97)
exe 'vert 4resize ' . ((&columns * 212 + 173) / 346)
argglobal
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 785 - ((17 * winheight(0) + 47) / 95)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
785
normal! 050|
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
let s:l = 219 - ((23 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
219
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
let s:l = 96 - ((13 * winheight(0) + 14) / 28)
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
let s:l = 3 - ((2 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 029|
lcd ~/Documents/communityvisweb/web/templates/fragments
wincmd w
exe 'vert 1resize ' . ((&columns * 133 + 173) / 346)
exe '2resize ' . ((&lines * 32 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 212 + 173) / 346)
exe '3resize ' . ((&lines * 28 + 48) / 97)
exe 'vert 3resize ' . ((&columns * 212 + 173) / 346)
exe '4resize ' . ((&lines * 33 + 48) / 97)
exe 'vert 4resize ' . ((&columns * 212 + 173) / 346)
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
let s:l = 26 - ((22 * winheight(0) + 44) / 89)
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
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 1resize ' . ((&columns * 128 + 173) / 346)
exe '2resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 212 + 173) / 346)
argglobal
setlocal fdm=expr
setlocal fde=pymode#folding#expr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 584 - ((46 * winheight(0) + 44) / 89)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
584
normal! 040|
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
let s:l = 157 - ((59 * winheight(0) + 44) / 89)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
157
normal! 032|
lcd ~/Documents/communityvisweb/web
wincmd w
exe '1resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 1resize ' . ((&columns * 128 + 173) / 346)
exe '2resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 212 + 173) / 346)
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
exe '1resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 1resize ' . ((&columns * 109 + 173) / 346)
exe '2resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 211 + 173) / 346)
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
let s:l = 75 - ((53 * winheight(0) + 44) / 89)
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
let s:l = 136 - ((81 * winheight(0) + 44) / 89)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
136
normal! 063|
lcd ~/Documents/communityvisweb/web
wincmd w
exe '1resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 1resize ' . ((&columns * 109 + 173) / 346)
exe '2resize ' . ((&lines * 89 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 211 + 173) / 346)
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
exe '1resize ' . ((&lines * 69 + 48) / 97)
exe 'vert 1resize ' . ((&columns * 121 + 173) / 346)
exe '2resize ' . ((&lines * 59 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 113 + 173) / 346)
exe '3resize ' . ((&lines * 9 + 48) / 97)
exe 'vert 3resize ' . ((&columns * 113 + 173) / 346)
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
let s:l = 5 - ((4 * winheight(0) + 34) / 69)
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
let s:l = 46 - ((45 * winheight(0) + 29) / 59)
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
exe '1resize ' . ((&lines * 69 + 48) / 97)
exe 'vert 1resize ' . ((&columns * 121 + 173) / 346)
exe '2resize ' . ((&lines * 59 + 48) / 97)
exe 'vert 2resize ' . ((&columns * 113 + 173) / 346)
exe '3resize ' . ((&lines * 9 + 48) / 97)
exe 'vert 3resize ' . ((&columns * 113 + 173) / 346)
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
let s:l = 74 - ((63 * winheight(0) + 44) / 89)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
74
normal! 045|
lcd ~/Documents/communityvisweb/web
tabnext 2
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
