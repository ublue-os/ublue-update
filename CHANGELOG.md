# Changelog

## [1.4.0](https://github.com/ublue-os/ublue-update/compare/v1.3.0...v1.4.0) (2024-05-02)


### Features

* Add topgrade support ([8a926c5](https://github.com/ublue-os/ublue-update/commit/8a926c5755d10aefc23480bc506b3936c2a7c58a))
* Add topgrade support ([#102](https://github.com/ublue-os/ublue-update/issues/102)) ([61dd86c](https://github.com/ublue-os/ublue-update/commit/61dd86c698e30c852c2cbd401bf407f9449553d8))
* Add updater for brew ([#76](https://github.com/ublue-os/ublue-update/issues/76)) ([63d40a1](https://github.com/ublue-os/ublue-update/commit/63d40a1688b52d4dcbcf37797ff14a355025c7fc))
* auto sign images ([#73](https://github.com/ublue-os/ublue-update/issues/73)) ([6acce45](https://github.com/ublue-os/ublue-update/commit/6acce45767dfd05e82c722c771b65400ce97cc82))
* move system update script to python ([#81](https://github.com/ublue-os/ublue-update/issues/81)) ([be229d1](https://github.com/ublue-os/ublue-update/commit/be229d1ee60dd7a5f7f5d0f118634bfa31918a88))
* Remove rebase step now that ISOs are nearly ready ([#105](https://github.com/ublue-os/ublue-update/issues/105)) ([1e670f0](https://github.com/ublue-os/ublue-update/commit/1e670f0044026b434da746bb28fa05a21fade00e))
* Remove rebase step now that ISOs are nearly ready, move topgrade configs to /usr/share, cleanup. ([8307b17](https://github.com/ublue-os/ublue-update/commit/8307b17a3c280431ffce863b7b98e74d31766cdb))
* **system-update:** Allow switching between branches via rebase ([e14f166](https://github.com/ublue-os/ublue-update/commit/e14f1665402a4e01a1778833c27568a07d48acfb))
* **system-update:** Allow switching between branches via rebase ([#91](https://github.com/ublue-os/ublue-update/issues/91)) ([e013061](https://github.com/ublue-os/ublue-update/commit/e013061013c97d5cf49d14237fdfe6b12ace8afe))


### Bug Fixes

* account for ostree-unverified-registry shorthand ([8271032](https://github.com/ublue-os/ublue-update/commit/8271032feed7b907d50520dfbc45afbc47d1cd6a))
* add brew to user and distrobox to system ([2e0e582](https://github.com/ublue-os/ublue-update/commit/2e0e582e125359108a910b5225f4daeb2e64a9bc))
* add brew to user and distrobox to system ([#107](https://github.com/ublue-os/ublue-update/issues/107)) ([d8fb315](https://github.com/ublue-os/ublue-update/commit/d8fb3157fac1f8c5836beae8ea97097c50403051))
* be more carefull when to rebase ([2ba442f](https://github.com/ublue-os/ublue-update/commit/2ba442f4be39dccf663dc1ae0c6696d6e738ca78))
* be more carefull when to rebase ([#88](https://github.com/ublue-os/ublue-update/issues/88)) ([427912c](https://github.com/ublue-os/ublue-update/commit/427912c53db77dab15f6e80c85f5d7a6118925b2))
* bump version ([32ccf70](https://github.com/ublue-os/ublue-update/commit/32ccf7082ed5228d2f55968eadf2469e4e1ef7f7))
* bypass distrobox upgrade sudo checks ([#69](https://github.com/ublue-os/ublue-update/issues/69)) ([127ed90](https://github.com/ublue-os/ublue-update/commit/127ed90804f2b56ba0191a7255edc9ff02a0754e))
* **flake8:** Ignore W503 and W504 ([5111b06](https://github.com/ublue-os/ublue-update/commit/5111b0643b146712117de9cae015f79296ee1646))
* Improve brew updater to work even if bash_profile change is missing ([#82](https://github.com/ublue-os/ublue-update/issues/82)) ([9993055](https://github.com/ublue-os/ublue-update/commit/99930556ea977fdf8234d84f45e402bdc162bbfa))
* min_battery_percent = 0 now works to "skip" ([5ad9228](https://github.com/ublue-os/ublue-update/commit/5ad9228568be47cd374e627a84008e609104d31d))
* min_battery_percent = 0 now works to "skip" battery check ([#89](https://github.com/ublue-os/ublue-update/issues/89)) ([c1f7355](https://github.com/ublue-os/ublue-update/commit/c1f735557c98f3483a96b81693571713a9f77305))
* offline iso update ([ea267e0](https://github.com/ublue-os/ublue-update/commit/ea267e044b47ee206620e59112bc5b0f2b8b623f))
* offline iso update ([#87](https://github.com/ublue-os/ublue-update/issues/87)) ([986ed9a](https://github.com/ublue-os/ublue-update/commit/986ed9a89bac290db79c393a2687794dce33827d))
* only show post update notification when there is a pending deployment ([#83](https://github.com/ublue-os/ublue-update/issues/83)) ([e117cc8](https://github.com/ublue-os/ublue-update/commit/e117cc89fd99b9438576cdd5e560afcef6c028d3))
* preserve unsigned image tag upon rebase ([0ff9fd5](https://github.com/ublue-os/ublue-update/commit/0ff9fd546607548e4aa15b82ca47bbe8c6ad14d4))
* preserve unsigned image tag upon rebase ([#75](https://github.com/ublue-os/ublue-update/issues/75)) ([75fd78b](https://github.com/ublue-os/ublue-update/commit/75fd78b0be2379185874074a4c0c5f2501ddd417))
* try to use staging copr project ([#71](https://github.com/ublue-os/ublue-update/issues/71)) ([2686474](https://github.com/ublue-os/ublue-update/commit/26864748cc9deca97a8387f33b4b8b95989b0a79))
* update error message logging, log subprocess output ([#77](https://github.com/ublue-os/ublue-update/issues/77)) ([007e1e3](https://github.com/ublue-os/ublue-update/commit/007e1e3b263c542c0510cc8bbb11272127fc3b75))

## [1.3.0](https://github.com/ublue-os/ublue-update/compare/v1.2.2...v1.3.0) (2023-09-20)


### Features

* **ci:** Split build for Fedora 38 and 39 ([#67](https://github.com/ublue-os/ublue-update/issues/67)) ([bd27a84](https://github.com/ublue-os/ublue-update/commit/bd27a84414aa917dbf4940defa062d9886164972))

## [1.2.2](https://github.com/ublue-os/ublue-update/compare/v1.2.1...v1.2.2) (2023-09-17)


### Bug Fixes

* change default max_mem_percent to 90.0 ([6119d3b](https://github.com/ublue-os/ublue-update/commit/6119d3b162ee72a28698ff501f7c7b6ead9c3594))
* formatting and errors ([53da743](https://github.com/ublue-os/ublue-update/commit/53da7431e5c4268519809c0d69bd4f1dd30a7aca))
* **hardware.py:** fixed memory check ([3f9aaec](https://github.com/ublue-os/ublue-update/commit/3f9aaec05fd04183f3eacdf1fef1b3260522c055))
* remove typo in arguments for notify-send ([41e3ed9](https://github.com/ublue-os/ublue-update/commit/41e3ed90b919891d98fd4a6b86a0bc3c04aa1831))
* remove typo in arguments for notify-send ([#61](https://github.com/ublue-os/ublue-update/issues/61)) ([0b0edf0](https://github.com/ublue-os/ublue-update/commit/0b0edf048a02a5a15ab9fb9c909383818dd2146e))
* skip copr-build on PRs ([9d1b30a](https://github.com/ublue-os/ublue-update/commit/9d1b30aecc9eb815eb34205f6a2128bd77f7ed37))

## [1.2.1](https://github.com/ublue-os/ublue-update/compare/v1.2.0...v1.2.1) (2023-09-04)


### Bug Fixes

* missing build requires python-pip ([#56](https://github.com/ublue-os/ublue-update/issues/56)) ([c583cae](https://github.com/ublue-os/ublue-update/commit/c583cae21c10eca1b7bf146f2ee066d65dc8af2a))

## [1.2.0](https://github.com/ublue-os/ublue-update/compare/v1.1.6...v1.2.0) (2023-09-02)


### Features

* Add module that waits for transaction completion before updating ([0abd5dc](https://github.com/ublue-os/ublue-update/commit/0abd5dccf0a805daed435ad791bfc94afd10a91c))
* Add module that waits for transaction completion before updating ([#55](https://github.com/ublue-os/ublue-update/issues/55)) ([d8d038b](https://github.com/ublue-os/ublue-update/commit/d8d038bb945a34b8c4fd562ba14c696355ea4ff4))
* Add support for updating with Fleek ([bcc731c](https://github.com/ublue-os/ublue-update/commit/bcc731cf609372ec54e5b5a0f692d8f895b01f0a))
* Add support for updating with Fleek ([#53](https://github.com/ublue-os/ublue-update/issues/53)) ([6bd7568](https://github.com/ublue-os/ublue-update/commit/6bd75682077d45f2cbf1b8c6a61c95a77cab5c43))


### Bug Fixes

* typo ([6d1a817](https://github.com/ublue-os/ublue-update/commit/6d1a817a9ebbb2d14603c1d1b2e3348c02ee4464))

## [1.1.6](https://github.com/ublue-os/ublue-update/compare/v1.1.5...v1.1.6) (2023-08-26)


### Bug Fixes

* update ublue_update_version macro to match version with github tag ([60ad5fd](https://github.com/ublue-os/ublue-update/commit/60ad5fd263253d2759e8d359b6bae94f55fae7ae))
* update ublue_update_version macro to match version with github tag ([#49](https://github.com/ublue-os/ublue-update/issues/49)) ([f0bbc04](https://github.com/ublue-os/ublue-update/commit/f0bbc048556680f710fae4b3906f0244b9c043dc))

## [1.1.5](https://github.com/ublue-os/ublue-update/compare/v1.1.4...v1.1.5) (2023-07-16)


### Bug Fixes

* Properly pull URL and tag from current image ([b0a35a2](https://github.com/ublue-os/ublue-update/commit/b0a35a2b1bc9d674cc651200afc0796bcdfc9150))
* Properly pull URL and tag from current image ([#46](https://github.com/ublue-os/ublue-update/issues/46)) ([aedb3cb](https://github.com/ublue-os/ublue-update/commit/aedb3cb8e55a8c64ce6580d9e8a3210500ca17ab))

## [1.1.4](https://github.com/ublue-os/ublue-update/compare/v1.1.3...v1.1.4) (2023-07-15)


### Bug Fixes

* added back Containerfile.builder to fix build action ([abf152e](https://github.com/ublue-os/ublue-update/commit/abf152ee44a36dbd5bbdb233fbd01c271c1abb3c))
* fix program exiting telling user checks have failed when running from notification ([7b24b8c](https://github.com/ublue-os/ublue-update/commit/7b24b8cb4b31a2406c55cc88e60a9a90bda1b173))
* fix program exiting telling user checks have failed when running from notification ([#43](https://github.com/ublue-os/ublue-update/issues/43)) ([2b42c62](https://github.com/ublue-os/ublue-update/commit/2b42c628660f3fa5999d8eb1542c919b9c44a087))
* fix updater throwing exception when dbus is inactive ([ee226b7](https://github.com/ublue-os/ublue-update/commit/ee226b7cfd164ec71487ea73b476eb8213775fb4))
* fixed and simplified argument behavior, use better naming ([3068671](https://github.com/ublue-os/ublue-update/commit/30686717c4e8ad5c4b369694d8f147718efa6656))
* formatting ([2a25ca0](https://github.com/ublue-os/ublue-update/commit/2a25ca02bbf18d1b8911107f04bb0f753783f115))
* make -c option work as intended ([c743b98](https://github.com/ublue-os/ublue-update/commit/c743b9844e1455ba07e33b159afee6c8a931f9df))
* move update logging into run_updates() function ([cb309ac](https://github.com/ublue-os/ublue-update/commit/cb309ac12863ac72fbbbe95372bbed542c16ecdf))
* reformat ([083a87a](https://github.com/ublue-os/ublue-update/commit/083a87a867bad87afc421e102031aaeff1f63b42))
* reformat to please the formatting gods ([38a18ec](https://github.com/ublue-os/ublue-update/commit/38a18ecbbf5a6c3bffeafc4d5e1668b4271d8d39))
* remove build remnent from git ([0e2fe81](https://github.com/ublue-os/ublue-update/commit/0e2fe8197cdc5b9a0debc61f07c5d209c7c8bf6e))
* remove ignores for **.md and **.txt ([837f0d5](https://github.com/ublue-os/ublue-update/commit/837f0d55e8ba7e540621ac6d941beec1ea411526))
* remove notification when system passes checks when running with -c ([0e1fa6e](https://github.com/ublue-os/ublue-update/commit/0e1fa6eedd18a86cef6c98aa90685e06a77e42a8))
* remove unnecessary if statement ([704e80e](https://github.com/ublue-os/ublue-update/commit/704e80e12e1f33e618fca4b880d6efdbcb55c41f))
* rename config file value to be loaded ([f5f7673](https://github.com/ublue-os/ublue-update/commit/f5f76732c8f2d7e37ca90e744b88430417fd2397))
* use os._exit() instead of sys.exit() to completely kill program ([abca773](https://github.com/ublue-os/ublue-update/commit/abca7739599b6bbb0cbef7b7312aed69c84e846f))

## [1.1.3](https://github.com/ublue-os/ublue-update/compare/v1.1.2...v1.1.3) (2023-07-15)


### Bug Fixes

* try to build release rpm ([83dfafa](https://github.com/ublue-os/ublue-update/commit/83dfafab19b46364aab689a4dc6b68d06f22f541))
* try to build release rpm ([#39](https://github.com/ublue-os/ublue-update/issues/39)) ([12b2ac2](https://github.com/ublue-os/ublue-update/commit/12b2ac2da57bfe35b29f96bf655365643c7a34cc))

## [1.1.2](https://github.com/ublue-os/ublue-update/compare/v1.1.1...v1.1.2) (2023-07-15)


### Bug Fixes

* build rpm in release workflow ([#38](https://github.com/ublue-os/ublue-update/issues/38)) ([c1517cc](https://github.com/ublue-os/ublue-update/commit/c1517ccd183fb0f67380ba4d8af68f1b358240ac))
* remove unnecessary documentation ([f6aeb24](https://github.com/ublue-os/ublue-update/commit/f6aeb24041558649c45815ba0bde67171ebb576e))
* remove unnecessary documentation ([#36](https://github.com/ublue-os/ublue-update/issues/36)) ([96fc700](https://github.com/ublue-os/ublue-update/commit/96fc7008cdece6b728ed4734c9b49e633ca7ec61))

## [1.1.1](https://github.com/ublue-os/ublue-update/compare/v1.1.0...v1.1.1) (2023-07-15)


### Bug Fixes

* use builder container file for release ([51b496a](https://github.com/ublue-os/ublue-update/commit/51b496a6a43ebfe3cb64ee5fbb2e308c79b9cb3c))

## [1.1.0](https://github.com/ublue-os/ublue-update/compare/v1.0.1...v1.1.0) (2023-07-09)


### Features

* added custom notification_manager to replace notify2 ([4b25c7c](https://github.com/ublue-os/ublue-update/commit/4b25c7c97a5f1f44a5d32e6df3a000e44cb02cfd))
* added NotificationObject, holds all notification data and makes it easier to deal with actions ([f67e3c9](https://github.com/ublue-os/ublue-update/commit/f67e3c905ae1ff19b988787cba6023cf410946ac))
* moved all dbus and glib logic into notification_manager ([d69ac11](https://github.com/ublue-os/ublue-update/commit/d69ac116351ce09a3839ea245f95998a3faa1e89))
* removed dependency on notify2 ([dc3325e](https://github.com/ublue-os/ublue-update/commit/dc3325e45aaafad6c9afe174b16971d66aef347a))


### Bug Fixes

* add extra spacing to please code formatter ([99fa0a3](https://github.com/ublue-os/ublue-update/commit/99fa0a370894001860b9333d1390985f93523fee))
* added import for DBusGMainLoop ([476c872](https://github.com/ublue-os/ublue-update/commit/476c872c58783487b9a045f1d2718590e7660543))
* fixed issues that prevented script from running, removed commented out code ([22b83c8](https://github.com/ublue-os/ublue-update/commit/22b83c850bf8dcb5dbba008f209a3f7705dc7579))
* fixed line length and corrected variable reference ([864e2ea](https://github.com/ublue-os/ublue-update/commit/864e2ea14872ca7c3d5b2f7b4d5848553425547f))
* import notification_manager module properly ([ebc387f](https://github.com/ublue-os/ublue-update/commit/ebc387fadfafefdc024b071fac54d8269a648902))

## [1.0.1](https://github.com/ublue-os/ublue-update/compare/v1.0.0...v1.0.1) (2023-07-06)


### Bug Fixes

* **config:** fix breakage when using fallback config, improved config logic to be more flexible ([f167dc9](https://github.com/ublue-os/ublue-update/commit/f167dc970d7b38e4ecf6d85895e800ce16760063))
* removed exit() and print() function used for debugging ([2eca189](https://github.com/ublue-os/ublue-update/commit/2eca1892a262ff7b1381dfcecb65d27fa5cd203e))

## 1.0.0 (2023-07-04)


### Features

* add log for when update is complete ([f3992f3](https://github.com/ublue-os/ublue-update/commit/f3992f39c5fae0db82e43e4192af67c7e9a7efce))
* add proof-of-concept containerfile for this project ([aeeb3c0](https://github.com/ublue-os/ublue-update/commit/aeeb3c08e459488b7dbd4a9737a3fa25f7f3a92a))
* add RPM build and restructure to make it work ([9642188](https://github.com/ublue-os/ublue-update/commit/9642188e94a1d0c147b9b78efa37fba324eb23a3))
* added --check option to run through update checks and exit ([ac0523b](https://github.com/ublue-os/ublue-update/commit/ac0523bea189c3216bdb45962d847a41169cdca1))
* made config loading more robust ([722c956](https://github.com/ublue-os/ublue-update/commit/722c956392235d268eacee803d1ccd00f930ab85))
* moved config format to toml, cleaned up config logic to default to /usr/etc ([2c47f12](https://github.com/ublue-os/ublue-update/commit/2c47f12d942b9b2c79c277369c9f015af67fd15d))


### Bug Fixes

* Adjust update service and timer ([2dc0ccc](https://github.com/ublue-os/ublue-update/commit/2dc0ccc80cdaa850c7acd2729e883118e2212ad5))
* apply some small python cleanups ([69e42d0](https://github.com/ublue-os/ublue-update/commit/69e42d0c74a2d5f0a78881ca1fd9494bad39c919))
* formatting errors after merge ([d3f011a](https://github.com/ublue-os/ublue-update/commit/d3f011ae4f46dce352ed46e61d20029845bd1fde))
* Make update scripts executable in spec file ([d57ea4e](https://github.com/ublue-os/ublue-update/commit/d57ea4ebbf080173d3cb9a56dbf89cd6bb1e11f5))
* moved log.info outside of if check ([ed25b1c](https://github.com/ublue-os/ublue-update/commit/ed25b1c3e17bcd8a64b2b60f26c73ba8a20bb404))
* remove 'sudo' from 'sudo install' in rpm spec ([8d80161](https://github.com/ublue-os/ublue-update/commit/8d801611a863338552a10047aa64cfb86be35b5f))
* remove unused makefile recipes ([93ea24a](https://github.com/ublue-os/ublue-update/commit/93ea24a290aaae4e66bec1397655c67ffcf4cf12))
* single line that makes the app not executable ([08706a5](https://github.com/ublue-os/ublue-update/commit/08706a546b8199bcad6ee1a611185e1ed1a82729))
* **systemd timer:** fixed spelling of persistent ([0c74fa2](https://github.com/ublue-os/ublue-update/commit/0c74fa24f8e7eab557fa7030571b671bee964b62))
* update comment ([3a6aff7](https://github.com/ublue-os/ublue-update/commit/3a6aff771def651f25fcbec6ff5504ae49666669))
* update install instructions to new image location ([eba75de](https://github.com/ublue-os/ublue-update/commit/eba75de2e56d96afd4b409427339206f242cb28e))
* use tabs not spaces ([7e33290](https://github.com/ublue-os/ublue-update/commit/7e332909d7a9443a0ba895515ac71b6fa7d3a56b))
* use the correct name ([2848f64](https://github.com/ublue-os/ublue-update/commit/2848f6434eaca1c71680e24250d03bf23a0c1504))

## 1.0.0 (2023-07-03)


### Features

* add log for when update is complete ([f3992f3](https://github.com/akdev1l/ublue-update/commit/f3992f39c5fae0db82e43e4192af67c7e9a7efce))
* add proof-of-concept containerfile for this project ([aeeb3c0](https://github.com/akdev1l/ublue-update/commit/aeeb3c08e459488b7dbd4a9737a3fa25f7f3a92a))
* add RPM build and restructure to make it work ([9642188](https://github.com/akdev1l/ublue-update/commit/9642188e94a1d0c147b9b78efa37fba324eb23a3))
* added --check option to run through update checks and exit ([ac0523b](https://github.com/akdev1l/ublue-update/commit/ac0523bea189c3216bdb45962d847a41169cdca1))
* made config loading more robust ([722c956](https://github.com/akdev1l/ublue-update/commit/722c956392235d268eacee803d1ccd00f930ab85))


### Bug Fixes

* apply some small python cleanups ([69e42d0](https://github.com/akdev1l/ublue-update/commit/69e42d0c74a2d5f0a78881ca1fd9494bad39c919))
* formatting errors after merge ([d3f011a](https://github.com/akdev1l/ublue-update/commit/d3f011ae4f46dce352ed46e61d20029845bd1fde))
* Make update scripts executable in spec file ([d57ea4e](https://github.com/akdev1l/ublue-update/commit/d57ea4ebbf080173d3cb9a56dbf89cd6bb1e11f5))
* moved log.info outside of if check ([ed25b1c](https://github.com/akdev1l/ublue-update/commit/ed25b1c3e17bcd8a64b2b60f26c73ba8a20bb404))
* remove 'sudo' from 'sudo install' in rpm spec ([8d80161](https://github.com/akdev1l/ublue-update/commit/8d801611a863338552a10047aa64cfb86be35b5f))
* remove unused makefile recipes ([93ea24a](https://github.com/akdev1l/ublue-update/commit/93ea24a290aaae4e66bec1397655c67ffcf4cf12))
* single line that makes the app not executable ([08706a5](https://github.com/akdev1l/ublue-update/commit/08706a546b8199bcad6ee1a611185e1ed1a82729))
* update comment ([3a6aff7](https://github.com/akdev1l/ublue-update/commit/3a6aff771def651f25fcbec6ff5504ae49666669))
* update install instructions to new image location ([eba75de](https://github.com/akdev1l/ublue-update/commit/eba75de2e56d96afd4b409427339206f242cb28e))
* use tabs not spaces ([7e33290](https://github.com/akdev1l/ublue-update/commit/7e332909d7a9443a0ba895515ac71b6fa7d3a56b))
* use the correct name ([2848f64](https://github.com/akdev1l/ublue-update/commit/2848f6434eaca1c71680e24250d03bf23a0c1504))
