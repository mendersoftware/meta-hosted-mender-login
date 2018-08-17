DESCRIPTION = "Mender GUI for logging in to Hosted Mender"

LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e3fc50a88d0a364313df4b21ef20c29e"

RPROVIDES_${PN} = "hosted-mender-login"
RDEPENDS_${PN} = "python-core python-requests python-pyqt5"
DEPENDS = "python-requests qtbase python-pyqt5 xserver-xorg"


SRC_URI = "file://menderLogin.py;subdir=${PN}-${PV} \
           file://menderLoginGUI.py;subdir=${PN}-${PV} \
           file://mender_logo.png;subdir=${PN}-${PV} \
           file://mender-hostedlogin.desktop;subdir=${PN}-${PV} \
           file://start-mender-hostedloginGUI.sh;subdir=${PN}-${PV} \
           file://LICENSE;subdir=${PN}-${PV} \
          "

do_install() {
    install -d ${D}${sysconfdir}/mender/login
    install -m 0644 menderLogin.py ${D}${sysconfdir}/mender/login
    install -m 0644 menderLoginGUI.py ${D}${sysconfdir}/mender/login
    install -m 0644 mender_logo.png ${D}${sysconfdir}/mender/login
    install -m 0755 start-mender-hostedloginGUI.sh ${D}${sysconfdir}/mender/login
    install -d ${D}${sysconfdir}/xdg/autostart
    install -m 0644 mender-hostedlogin.desktop ${D}${sysconfdir}/xdg/autostart
}
