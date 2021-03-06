" syntax/lsl.vim
" LSL Syntax File
" Language: lsl
" Maintainer: PumpkinPai <pumpkin@luvotron.com>
" Last update: LASTUPDATE
" Credits:
"         Builder's Brewery maintains a set of lsl syntax files in
"               https://github.com/buildersbrewery/lsl-for-vim
"           and https://github.com/buildersbrewery/linden-scripting-language
"         The idea for this plugin was ultimately from those projects


if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

" nocompatible mode for lines with backslashes
let s:cpo_save = &cpo
set cpo&vim




" COMMENTS "
syntax keyword lslTodo
\ todo Todo TODO fixme Fixme FIXME bug Bug BUG xxx XXX

" DEBUGGING "
syntax keyword lslDebug
\ debug Debug DEBUG temp Temp TEMP

" FUNCTIONS "
syn keyword lslFunction
\ !!LSL_FUNCTIONS!!

" EVENTS "
syn keyword lslEvent
\ !!LSL_EVENTS!!

" CONSTANTS "
syn keyword lslConstant
\ !!LSL_CONSTANTS!!

" DEPRECATED "
syn keyword lslDeprecated
\ !!LSL_DEPRECATED!!

" CONDITIONAL "
syn keyword lslConditional
\ if
\ else

" REPEATS "
syn keyword lslRepeat
\ do
\ while
\ for
\ jump
\ return

" TYPES "
syn keyword lslType
\ key
\ string
\ list
\ integer
\ float
\ vector
\ rotation

" LABELS "
syn keyword lslLabel
\ state default

" DISPLAYS "
syn match lslNumber display
\ /[0-9]/

syn region lslString display
\ start='"' skip='//.' end='"' contains=lslStringEscape, @Spell

syn match lslStringEscape display
\ /\\t\|\\n/

syn region lslBlock
\ start='{' end='}' fold transparent contains=ALL

syn region lslParen display
\ start='(' end=')' fold transparent contains=ALL

syn region lslList display
\ start='\[' end='\]' fold transparent contains=ALL

syn match lslState display
\ /\b(state)[' ']\w*/ contains=lslLabel

syn region lslComment display
\ start='\/\/' end='$' contains=lslTodo,@Spell

syn region lslCommentMulti display
\ start='\/\*' end='\*\/' contains=lslTodo,@Spell

syn match lslOperator display
\ /[!%<>=*\+\-\|&\?\^~]/

syn match lslOperator display
\ /\/\(\/\)\@!/

" HIGHLIGHTING "
highlight default link lslTodo          Todo
highlight default link lslDebug         Special
highlight default link lslComment       Comment
highlight default link lslCommentMulti  Comment

highlight default link lslFunction      Function
highlight default link lslEvent         Function
highlight default link lslConstant      Constant
highlight default link lslDeprecated    Error

highlight default link lslType          Type
highlight default link lslConditional   Conditional
highlight default link lslRepeat        Repeat
highlight default link lslLabel         Label
highlight default link lslOperator      Operator

highlight default link lslString        String
highlight default link lslStringEscaped Special
highlight default link lslNumber        Number
highlight default link lslKey           Special
highlight default link lslState         Label

highlight default link lslParen         Special
highlight default link lslBlock         Special
highlight default link lslList          Special


let b:current_syntax = "lsl"

let &cpo = s:cpo_save
unlet s:cpo_save

