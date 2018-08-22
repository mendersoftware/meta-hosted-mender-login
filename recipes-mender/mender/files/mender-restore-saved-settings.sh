#!/bin/sh
#

SAVED_SETTINGS_FILE=/data/mender/hosted-mender-settings.dat
MENDER_CONF_FILE=/etc/mender/mender.conf

if [ -e "${SAVED_SETTINGS_FILE}" ]; then
    # Restore any settings that are relevant.
    # These will have been saved here by the menderLogin.py script.
    SAVED_TENANT_TOKEN=$(head -n 1 ${SAVED_SETTINGS_FILE})
    SAVED_SERVER_URL=$(tail -n 1 ${SAVED_SETTINGS_FILE})

    # If we have the dummy value for the TenantToken but we have a saved
    # value, then add the saved value into the mender conf file
    # This generally means that an OTA update was performed and the
    # unmodified conf file was installed.
    if grep -q TenantToken.*dummy "${MENDER_CONF_FILE}"; then
        sed -i "s@\"TenantToken\": \"dummy\",@\"TenantToken\": \"${SAVED_TENANT_TOKEN}\",@" "${MENDER_CONF_FILE}"
    fi

    # Similar test for the Server URL
    if grep -q ServerURL.*dummy "${MENDER_CONF_FILE}"; then
        sed -i "s@\"ServerURL\": \"dummy\",@\"ServerURL\": \"${SAVED_SERVER_URL}\",@" "${MENDER_CONF_FILE}"
    fi
 fi
