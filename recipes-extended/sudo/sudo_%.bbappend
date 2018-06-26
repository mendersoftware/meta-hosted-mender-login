FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

FILES_${PN} += "${sysconfdir}/sudoers"


do_install_append() {
    bbwarn "Appending \"user    ALL=(ALL:ALL) NOPASSWD:/bin/mv /tmp/mender.conf.tmp /etc/mender/mender.conf\" to /etc/sudoers"
    echo "user    ALL=(ALL:ALL) NOPASSWD:/bin/mv /tmp/mender.conf.tmp /etc/mender/mender.conf" >> ${D}${sysconfdir}/sudoers
}
