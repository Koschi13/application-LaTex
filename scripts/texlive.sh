#!/usr/bin/env bash

GIT_ROOT=$(git rev-parse --show-toplevel)
# [!IMPORTANT] Sync with `templates/meta.tex`
OUTPUT_DIR="${GIT_ROOT}/build"
SOURCE_DIR="${GIT_ROOT}/example"

pushd $GIT_ROOT

  cd templates \
  && rm -r $OUTPUT_DIR \
  && mkdir -p $OUTPUT_DIR \
  && printf "\n################################################################################\nBulding letter.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${OUTPUT_DIR} "\def\sourceDir{${SOURCE_DIR}} \def\outputDir{${BUILD_DIR}} \input{letter.tex}" \
  && printf "\n################################################################################\nBulding cv.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${OUTPUT_DIR} "\def\sourceDir{${SOURCE_DIR}} \def\outputDir{${BUILD_DIR}} \input{cv.tex}" \
  && printf "\n################################################################################\nBulding cv.tex again to get page numbers right...\n################################################################################\n\n" \
  && pdflatex --output-directory=${OUTPUT_DIR} "\def\sourceDir{${SOURCE_DIR}} \def\outputDir{${BUILD_DIR}} \input{cv.tex}" \
  && printf "\n################################################################################\nBulding application.tex...\n################################################################################\n\n" \
  && pdflatex --output-directory=${OUTPUT_DIR} "\def\sourceDir{${SOURCE_DIR}} \def\outputDir{${BUILD_DIR}} \input{application.tex}" \

popd

