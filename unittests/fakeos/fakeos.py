
class FakeFs(object):

  def __init__(self, fakefsdata, cwd):
    self.fakefsdata = fakefsdata
    self.cwd = cwd

class FakePathMod(object):

  def __init__(self, fakefs):
    self.fakefs = fakefs

class FakeOsMod(object):

  def __init__(self, fakefs, fakepathmod):
    self.fakefs = fakefs
    self.path = fakepathmod

  def getcwd(self):
    return self.fakefs.cwd

def fakeos(fakefsdata, cwd):
  fakefs = FakeFs(fakefsdata, cwd)
  fakepathmod = FakePathMod(fakefs)
  fakeosmod = FakeOsMod(fakefs, fakepathmod)
  return fakeosmod
