#! /bin/bash

# CK installation script
#
# Developer(s):
#  * Grigori Fursin, dividiti/cTuning foundation
#

# PACKAGE_DIR
# INSTALL_DIR
######################################################################################
echo "Installing CK-QUANTUM HACKATHON MODULE"
echo ""



if [ ! -d "${INSTALL_DIR}/lib" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir -p ${INSTALL_DIR}/lib
fi

cp -r ${PACKAGE_DIR}/hackathon-src/*  ${INSTALL_DIR}/lib/


if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

######################################################################################

