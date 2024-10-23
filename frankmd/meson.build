pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'frankmd'
gnome = import('gnome')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

subdir('resources')
subdir('app')
subdir('widgets')

configure_file(
  input: 'frankmd.in',
  output: 'frankmd',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

frankmd_sources = [
  '__init__.py',
  'main.py',
]

install_data(frankmd_sources, install_dir: moduledir)
