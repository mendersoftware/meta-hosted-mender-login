FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

FILES_${PN} += "${sysconfdir}/sudoers"


do_install_append() {
    # Add exceptions to overwrite mender.conf and disable autostart.
    bbwarn "Appending \"user    ALL=(ALL:ALL) NOPASSWD:/bin/mv /tmp/mender.conf.tmp /etc/mender/mender.conf\" to /etc/sudoers"
    echo "user    ALL=(ALL:ALL) NOPASSWD:/bin/mv /tmp/mender.conf.tmp /etc/mender/mender.conf" >> ${D}${sysconfdir}/sudoers
    bbwarn "Appending \"user    ALL=(ALL:ALL) NOPASSWD:/bin/mv /etc/xdg/autostart/mender-hostedlogin.desktop /etc/mender/login/mender-hostedlogin.desktop\" to /etc/sudoers"
    echo "user    ALL=(ALL:ALL) NOPASSWD:/bin/mv /etc/xdg/autostart/mender-hostedlogin.desktop /etc/mender/login/mender-hostedlogin.desktop" >> ${D}${sysconfdir}/sudoers
}
