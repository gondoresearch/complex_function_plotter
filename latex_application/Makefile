MAINFILE = main
BUILDDIR = build
OUTPUT_OPTS = max_print_line=400

TEXENGINE = pdflatex
TEXENGINE_OPTS = --output-directory=${BUILDDIR} --shell-escape 

# ANSI terminal colors (see 'man tput') and
# https://linuxtidbits.wordpress.com/2008/08/11/output-color-on-bash-scripts/
#
# Don't use color if there isn't a $TERM environment variable:
ifneq ($(strip $(TERM)),)
	BOLD=$(shell tput bold)
	RED=$(shell tput setaf 1)
	GREEN=$(shell tput setaf 2)
	BLUE=$(shell tput setaf 4)
	MAGENTA=$(shell tput setaf 5)
	WHITE=$(shell tput setaf 7)
	UL=$(shell tput sgr 0 1)
	RESET=$(shell tput sgr0 )
endif

# Calling the engine only
pdf:	
	@echo "$(BOLD)Compiling$(RESET) ${MAINFILE}.tex at \"${BUILDDIR}\" folder using ${TEXENGINE} engine ...$(RESET)"
	@$(MAKE) -s check
	@$(OUTPUT_OPTS) $(TEXENGINE) $(TEXENGINE_OPTS) $(MAINFILE).tex -enable-write18

# Checks if BUILDDIR exists. If not, creates it.
check:
	@if [ ! -d ${BUILDDIR} ] ; then \
		echo -n "$(BOLD)BUILDDIR check: $(RED)BUILDDIR not found$(WHITE). Creating it...$(RESET)" ; \
		mkdir ${BUILDDIR} ; \
		echo "	$(GREEN)Done.$(RESET)" ; \
	fi
