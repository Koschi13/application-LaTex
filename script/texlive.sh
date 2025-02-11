#!/usr/bin/env bash

GIT_ROOT=$(git rev-parse --show-toplevel)
# NOTE: This must be within the direcotry of the files, otherwise the build will fail
BUILD_DIR="build/"

pushd $GIT_ROOT

  cd Vorlage \
  && mkdir -p $BUILD_DIR \
  && printf "\n################################################################################\nBulding anschreiben.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${BUILD_DIR} anschreiben.tex \
  && printf "\n################################################################################\nBulding cv.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${BUILD_DIR} cv.tex \
  && printf "\n################################################################################\nBulding anhang.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${BUILD_DIR} anhang.tex \
  && printf "\n################################################################################\nBulding Bewerbung_Einzeln.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${BUILD_DIR} Bewerbung_Einzeln.tex \
  && printf "\n################################################################################\nBulding Bewerbung_Komplett.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${BUILD_DIR} --shell-escape ./Bewerbung_Komplett.tex 

popd
