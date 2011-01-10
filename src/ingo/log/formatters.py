import logging
try:
    import curses
    
    if sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                curses = None
        except:
            pass
except:
    curses = None

class ColorFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        if curses:
            fg_color = curses.tigetstr("setaf") or curses.tigetstr("setf") or ""
            self._colors = {
                logging.DEBUG: curses.tparm(fg_color, 4), # Blue
                logging.INFO: curses.tparm(fg_color, 2), # Green
                logging.WARNING: curses.tparm(fg_color, 3), # Yellow
                logging.ERROR: curses.tparm(fg_color, 1), # Red
            }
            self._normal = curses.tigetstr("sgr0")

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception, e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        record.asctime = time.strftime(
            "%y%m%d %H:%M:%S", self.converter(record.created))
        prefix = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]' % \
            record.__dict__
        if curses:
            prefix = (self._colors.get(record.levelno, self._normal) +
                      prefix + self._normal)
        formatted = prefix + " " + record.message
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = formatted.rstrip() + "\n" + record.exc_text
        return formatted.replace("\n", "\n    ")