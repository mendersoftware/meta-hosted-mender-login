FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

MENDER_SERVER_URL = "dummy"

SRC_URI += " \
    file://mender-restore-saved-settings.sh \
"

FILES_${PN} += " \
     ${sbindir}/mender-restore-saved-settings.sh \
"

do_install_prepend() {
    # Update the service file to invoke mender-generate-certificate
    cat >> ${WORKDIR}/${SYSTEMD_SERVICE_${PN}} <<-EOF

	[Service]
	ExecStartPre=${sbindir}/mender-restore-saved-settings.sh
	EOF
}

do_install_append() {
    install -d ${D}${sbindir}
    install -m 0755 ${WORKDIR}/mender-restore-saved-settings.sh ${D}${sbindir}
}
