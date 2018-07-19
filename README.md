# meta-hosted-mender-login

This Yocto meta layer contains all the recipes needed to build the GUI for logging in to Hosted Mender. The application will launch on boot prompting for Hosted Mender credentials, the application fetches your `TenantToken` and places it in to the Mender configuration file.

This layer depends on [meta-qt5](http://layers.openembedded.org/layerindex/branch/master/layer/meta-qt5/) and [meta-python](http://layers.openembedded.org/layerindex/branch/master/layer/meta-python/), and an image with a graphical environment.

## Contributing

We welcome and ask for your contribution. If you would like to contribute to Mender, please read our guide on how to best get started [contributing code or documentation](https://github.com/mendersoftware/mender/blob/master/CONTRIBUTING.md).
