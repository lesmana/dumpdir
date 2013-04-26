
class FakeFs(object):

  def __init__(self, fakefsdata):
    self.fakefsdata = fakefsdata

class FakePathMod(object):

  def __init__(self, fakefs):
    self.fakefs = fakefs

class FakeOsMod(object):

  def __init__(self, fakefs, cwd, fakepathmod):
    self.fakefs = fakefs
    self.cwd = cwd
    self.path = fakepathmod

  def getcwd(self):
    return self.cwd

def fakeos(fakefsdata, cwd):
  fakefs = FakeFs(fakefsdata)
  fakepathmod = FakePathMod(fakefs)
  fakeosmod = FakeOsMod(fakefs, cwd, fakepathmod)
  return fakeosmod
