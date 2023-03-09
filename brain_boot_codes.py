# Various collection of codes

CLEAR_DISPLAY = "01u"

# Write the D8B 5.1 / MACKIE DIGITAL welcome string.
WELCOME_STRING1 = "90u44v38v42v" 
WELCOME_STRING2 = "94u35v2Ev31v"
WELCOME_STRING3 = "CDu4Dv41v43v4Bv49v45v"
WELCOME_STRING4 = "D4u44v49v47v49v54v41v4Cv"

# this writes: TAPE A   TAPE B   TAPE C    ALTIO with a dash under each.
# the xxu is a "cursor position" in the display. 
# the xxp are ascii hex charachters
TAPE_LIST = "81u54v41v50v45v86u41v8Bu54v41v50v45v90u42v20v20v94u20v54v41v50v45v9Au43vA0u41v4Cv54v49v4FvC4u2DvCDu20v2Dv20v20v20v20vD4u20v20v20v20v2Dv20v20vE2u2Dv"

# These commands writes "OPT-8" under the TAPE X's
TAPE_A_OPT8 = "C2u4Fv50v54v2Dv38v"
TAPE_B_OPT8 = "CCu4Fv50v54v2Dv38v"
TAPE_C_OPT8 = "D6u4Fv50v54v2Dv38v"
ALT_IO_OPT8 = "E0u4Fv50v54v2Dv38v"

# This next command write:
# STEREO WORD CLOCK
# AES-2      -
STEREO_WORD_CLOCK_AES ="81u20v20v20v20v86u20v8Bu20v20v20v20v90u20v95u20v20v20v20v9Au20vA0u20v20v20v20v20vC2u20v20v20v20v20vCCu20v20v20v20v20vD6u20v20v20v20v20vE0u20v20v20v20v20v82u53v54v45v52v45v4Fv8Au57v4Fv52v44v8Fu43v4Cv4Fv43v4BvC4u2DvCEu2DvC2u41v45v53v2Dv32v"

# ... what it says...
MACKIE_UNDER_WORDCLOCK ="CCu4Dv61v63v6Bv69v65v"

# Loading DSP plugins...
LOADING_DSP = "80u4Cv6Fv61v64v69v6Ev67v20v44v53v50v20v50v6Cv75v67v69v6Ev73v2Ev2Ev2EvC2u20v20v20v20v20vCCu20v20v20v20v20v20v"

# Display the FX card lidt
FX_CARD_LIST = "80u20v46v58v43v61v72v64v88u41v20v20v46v58v43v61v72v64v20v42v20v20v46v58v43v61v72v64v9Cu43v9Fu46v58v43v61v72v64vA6u44vC4u2DvCEu2DvD8u2DvE2u2Dv" 

# Commands for checking if a slot has an MFX card
FXA_QUERY_MFX = "F0q00q00q0Bq00q41q59q42q00q30q00q01q01q00q32qF7q"
FXB_QUERY_MFX = "F0q00q00q0Bq00q45q59q42q00q30q00q01q01q00q32qF7q"
FXC_QUERY_MFX = "F0q00q00q0Bq00q49q59q42q00q30q00q01q01q00q32qF7q"
FXD_QUERY_MFX = "F0q00q00q0Bq00q4Dq59q42q00q30q00q01q01q00q32qF7q"

FX_MFX_QUERIES = {
    "a" : "F0q00q00q0Bq00q41q59q42q00q30q00q01q01q00q32qF7q",
    "b" : "F0q00q00q0Bq00q45q59q42q00q30q00q01q01q00q32qF7q",
    "c" : "F0q00q00q0Bq00q49q59q42q00q30q00q01q01q00q32qF7q",
    "d" : "F0q00q00q0Bq00q4Dq59q42q00q30q00q01q01q00q32qF7q"
}

# Responses, in case slot holds an MFX card:
FXA_MFX_REPLY = "F0q00q00q0Bq00q41q58q00qF7q"
FXB_MFX_REPLY = "F0q00q00q0Bq00q45q58q00qF7q" 
FXC_MFX_REPLY = "F0q00q00q0Bq00q49q58q00qF7q"
FXD_MFX_REPLY = "F0q00q00q0Bq00q4Dq58q00qF7q"

# Commands for checking if slot has a UFX card
FXA_QUERY_UFX = "F0q00q00q50q00q40q59qF7q"
FXB_QUERY_UFX = "F0q00q00q50q04q44q59qF7q"
FXC_QUERY_UFX = "F0q00q00q50q08q48q59qF7q"
FXD_QUERY_UFX = "F0q00q00q50q0Cq4Cq59qF7q"

# Responses, in case slot holds a UFX card:
FXA_UFX_REPLY = "F0q00q00q50q00q40q58q05q00q00q00qF7q"
FXB_UFX_REPLY = "F0q00q00q50q04q44q58q05q00q00q00qF7q"
FXC_UFX_REPLY = "F0q00q00q50q08q48q58q05q00q00q00qF7q"
FXD_UFX_REPLY = "F0q00q00q50q0Cq4Cq58q05q00q00q00qF7q"

# If a UFX card is detected, two more commands are sent. Unsure exactly what they are... maybe some init stuff?
FXA_UFX_CMD1 = "F0q00q00q50q00q40q4FqF7q"
FXA_UFX_CMD2 = "F0q00q00q50q02q42q4FqF7q"

FXB_UFX_CMD1 = "F0q00q00q50q04q44q4FqF7q" 
FXB_UFX_CMD2 = "F0q00q00q50q06q46q4FqF7q"

FXC_UFX_CMD1 = "F0q00q00q50q08q48q4FqF7q" 
FXC_UFX_CMD2 = "F0q00q00q50q0Aq4Aq4FqF7q"

FXD_UFX_CMD1 = "F0q00q00q50q0Cq4Cq4FqF7q"
FXD_UFX_CMD2 = "F0q00q00q50q0Eq4Eq4FqF7q"

# Display strings for "emtpy" fx slot:
FXA_EMPTY = "C2u65v6Dv70v74v79v"
FXB_EMPTY = "CCu65v6Dv70v74v79v"
FXC_EMPTY = "D6u65v6Dv70v74v79v"
FXD_EMPTY = "E0u65v6Dv70v74v79v"

# Display strings for having an MFX
FXA_GOT_MFX = "C3u4Dv46v58v"
FXB_GOT_MFX = "CDu4Dv46v58v"
FXC_GOT_MFX = "D7u4Dv46v58v"
FXD_GOT_MFX = "E1u4Dv46v58v"

# Display strings for having an UFX
FXA_GOT_UFX = "C3u55v46v58v"
FXB_GOT_UFX = "CDu55v46v58v"
FXC_GOT_UFX = "D7u55v46v58v"
FXD_GOT_UFX = "E1u55v46v58v"


