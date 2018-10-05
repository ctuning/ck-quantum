#!/usr/bin/env python3

import time
import curses
import sys, os
import select
from math import *
from ast import literal_eval
import ap
import numpy as np
from functools import partial
import subprocess
import json
import threading

try:
    import inotify
    NOTIFY_AVAILABLE = True
except ImportError:
    NOTIFY_AVAILABLE = False

# just run in a thread.
class DataSource(threading.Thread):
    """Class for obtaining data from the log saved by ck run.

    we (try) to open the file, stream in the data from it.
    if ck run is restarted, the file will be unlinked - we need to detect
    this and discard prev data.
    """

    def __init__(self, fname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fname = fname
        self.logs = None # [[0, 1, 2, 3, 4, 5], [0.5, 1.5, 2.5, 3.5]]
        self.running = False
        self.file = None
        self.Nruns = 0

    def run(self):
        """Loads data from a file, and monitors it for changes.

        if the file is removed, then a new ck run command has begun.
        we need to discard the current data, and begin monitoring the new file.
        """
        self.running = True
        while self.running:
            # os.stat to see if the file is zero length
            # os.fstat(f.fileno()).st_nlink == 0? file anon, need to reopen
            if self.file is not None and os.fstat(self.file.fileno()).st_nlink == 0:
                # file has been unlinked
                self.file = None # kill it.

            elif self.file is not None: # have a file object, should be valid. try and read more data from it.
                line = self.file.readline()
                if line == '': #eof
                    time.sleep(0.1) # wait a bit
                elif line.startswith('{'): # experimental iteration.
                    d = literal_eval(line)
                    self.logs[-1].append(d["energy"])
                elif line.startswith('#'):
                    self.logs.append([]) # new experiment run

            else:
                try:
                    self.file = open(self.fname, "r")
                    self.logs = [[]]
                except FileNotFoundError:
                    if not NOTIFY_AVAILABLE:
                        time.sleep(0.1)
                    else:
                        # can do somthing fancy.
                        time.sleep(0.1)


class CURSESDisplay(threading.Thread):

    stats_format = """N runs = {nruns}
Minimum energy seen = {mine}
Final mean = {mean}
Final variance = {var}
"""

    def __init__(self, datasource, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = datasource


    def run(self):
        curses.wrapper(self._main)

    def draw_stats(self, window):
        window.clear()

        if self.data.logs:
            final_es = []
            min_ = 0
            for i, log in enumerate(self.data.logs):
                if log:
                    min_ = min(min_, min(log))
                if log and i != len(self.data.logs)-1: # for finished runs
                    final_es.append(min(log))

            window.addstr(self.stats_format.format(
                nruns = len(self.data.logs)-1,
                mine = min_,
                mean = np.mean(final_es) if len(final_es) > 1 else "Insufficent data",
                var = np.std(final_es) if len(final_es) > 1 else "Insufficent data"
            ))
        else:
            window.addstr("No data yet!")




    def draw_graphs(self, window):
        """Draws data from self.datasource to a curses window.
        """
        height,width = window.getmaxyx()

        if self.data.logs:
            min_, max_ = -1.7, -1.6
            p = ap.AFigure(shape=(width-2, height-3))
            # p.xlabel("optimiser iteration")
            # p.ylabel("Energy")
            for i, log in enumerate(self.data.logs):
                if len(log) < 1:
                    continue
                marker = '_,' if i == len(self.data.logs)-1 else '_.'
                x = np.arange(len(log))
                y = log
                _ = p.plot(x, y, marker=marker, plot_slope=False)
                min_ = min(min_, min(log))
                max_ = max(max_, max(log))

            p.ylim(min_, max_)
            plot_str = p.draw()

            for i, line in enumerate(plot_str.split("\n")):
                window.addstr(i,0,line)


    def _main(self, stdscr):
        """Draws the CURSES ui.
        """

        graph_size = ceil(curses.LINES * (2/3))
        echo_v_size = floor(curses.LINES * (1/3))

        stats_border = curses.newwin(echo_v_size, curses.COLS, graph_size, 0)
        stats = stats_border.derwin(echo_v_size-2, curses.COLS-2, 1, 1)

        graph_border = curses.newwin(graph_size, curses.COLS, 0, 0)
        graphwin = graph_border.derwin(graph_size-2, curses.COLS-2, 1, 1)

        # graphwin.scrollok(True)
        stdscr.nodelay(True)
        graph_border.border()
        stats_border.border()
        stats_border.addstr(0, 2, "stats")

        logs = []
        running = True

        while running:

            stdscr.refresh()

            graphwin.refresh()
            graph_border.refresh()
            stats_border.refresh()
            stats.refresh()

            graphwin.move(0,0)

            # noblock
            cmd = stdscr.getch()
            if cmd == ord('q'):
                break

            self.draw_graphs(graphwin)
            self.draw_stats(stats)
            graph_border.addstr(0,20,"Optimiser iteration")
            for i,c in enumerate("Energy"):
                graph_border.addstr(10+i,0,c)

            # will ahve some kind of update polling mech, but not yet
            time.sleep(0.1)


def get_fname():
    """Uses CK to get the file that contains the live-updated iteration progress.
    """

    if 'CK_ROOT' in os.environ:
        import sys
        sys.path.append( os.environ['CK_ROOT'] )

    import ck.kernel as ck

    load_adict = {  'action':           'load',
                    'module_uoa':       'program',
                    'data_uoa':         'qiskit-vqe',
    }
    r=ck.access( load_adict )
    if r['return']>0: return r

    program_entry_path  = r['path']
    stream_file_path    = os.path.join( program_entry_path, 'tmp', 'vqe_stream.json')

    return stream_file_path


if __name__ == "__main__":

    # now we get input from a file, don't allow pipes to stdin
    if not sys.stdin.isatty():
        print("please run interactively.")
        sys.exit(1)

    fname = sys.argv[1] if len(sys.argv) > 1 else get_fname()
    data = DataSource(fname)
    ui = CURSESDisplay(data)
    data.start()
    ui.start()
    ui.join()
    data.running = False
    data.join()
