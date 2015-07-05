# Maintainer: Chris Warrick <aur@chriswarrick.com>
pkgbase=python-upass
pkgname=('python-upass' 'python2-upass')
_pyname=upass
pkgver=0.1.0
pkgrel=1
pkgdesc='Console UI for pass'
arch=('any')
url='https://github.com/Kwpolska/upass'
license=('BSD')
makedepends=('python' 'python2' 'python-setuptools' 'python2-setuptools'
             'python-urwid' 'python2-urwid' 'python-pyperclip'
             'python2-pyperclip')
options=(!emptydirs)
source=("https://pypi.python.org/packages/source/${_pyname:0:1}/${_pyname}/${_pyname}-${pkgver}.tar.gz")
md5sums=('7e885f7b9239226990fbe9f2f6baf444')

prepare() {
  cd "${srcdir}/${_pyname}-${pkgver}"
  cp -r "${srcdir}/${_pyname}-${pkgver}" "${srcdir}/${_pyname}-${pkgver}-py2"
}

package_python-upass() {
  depends=('python' 'python-setuptools' 'python-urwid' 'python-pyperclip')
  cd "${srcdir}/${_pyname}-${pkgver}"
  python3 setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgbase}/LICENSE"
}

package_python2-upass() {
  depends=('python2' 'python2-setuptools' 'python2-urwid' 'python2-pyperclip')
  cd "${srcdir}/${_pyname}-${pkgver}-py2"
  python2 setup.py install --root="${pkgdir}/" --optimize=1
}

# vim:set ts=2 sw=2 et:
