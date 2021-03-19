pkg_name=culture_dispenser
pkg_origin=nrgetik
pkg_version="0.1.0"
pkg_maintainer="The Habitat Maintainers <humans@habitat.sh>"
pkg_license=("Apache-2.0")
# pkg_scaffolding="some/scaffolding"
# pkg_source="http://some_source_url/releases/${pkg_name}-${pkg_version}.tar.gz"
# pkg_filename="${pkg_name}-${pkg_version}.tar.gz"
# pkg_shasum="TODO"
# pkg_deps=(core/glibc)
pkg_deps=(core/coreutils core/python/3.7.0)
# pkg_build_deps=(core/make core/gcc)
pkg_build_deps=(core/make core/gcc)
# pkg_lib_dirs=(lib)
# pkg_include_dirs=(include)
# pkg_bin_dirs=(bin)
# pkg_pconfig_dirs=(lib/pconfig)
# pkg_description="Some description."
# pkg_upstream_url="http://example.com/project-name"

do_verify() {
  return 0
}

do_build() {
  pip install requests
  pip install ratelimit
  pip install flask
  pip install unqlite
}

do_install() {
  cp $PLAN_CONTEXT/../*.py $pkg_prefix
  cp $PLAN_CONTEXT/../*.sh $pkg_prefix
  cp -r $PLAN_CONTEXT/../templates $pkg_prefix
  cp -r $PLAN_CONTEXT/../__pycache__ $pkg_prefix
  cp $PLAN_CONTEXT/../artsy.db $pkg_prefix
  # fix_interpreter $pkg_prefix/artsy_db.py core/coreutils bin/env
  # fix_interpreter $pkg_prefix/populate_artsy_db.py core/coreutils bin/env
  # fix_interpreter $pkg_prefix/pull_artsy_images.py core/coreutils bin/env
  # fix_interpreter $pkg_prefix/process_images.sh core/coreutils bin/env
}
