"""Linux CPU jobs in a private subreaper supervisor; no exception/output leakage."""
import ctypes
import multiprocessing
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time


def _snapshot():
    result={}
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            fields=path.read_text().rsplit(') ',1)[1].split()
            result[int(path.parent.name)]=(int(fields[1]),fields[19],fields[0])
        except (OSError,ValueError,IndexError): pass
    return result


def _descendants():
    """Private supervisor owns every descendant, including adopted double forks."""
    records=_snapshot();parents={os.getpid()};found={}
    while True:
        children={pid:identity for pid,(parent,identity,state) in records.items()
                  if parent in parents and pid not in parents and state!='Z'}
        if not children: return found
        found.update(children);parents.update(children)


def _signal(records, sig):
    for pid,identity in records.items():
        fd=None
        try:
            fd=os.pidfd_open(pid)
            # Pin first, then confirm identity; signals cannot hit a reused PID.
            fields=Path(f'/proc/{pid}/stat').read_text().rsplit(') ',1)[1].split()
            if fields[19]==identity: signal.pidfd_send_signal(fd,sig)
        except (ProcessLookupError,FileNotFoundError): pass
        finally:
            if fd is not None: os.close(fd)


def _cleanup(process):
    _signal(_descendants(),signal.SIGTERM)
    if process is not None:
        try: process.wait(timeout=3)
        except subprocess.TimeoutExpired: pass
    # Exiting leaders reparent detached children to this supervisor, never PID 1.
    for _ in range(100):
        remaining=_descendants()
        _signal(remaining,signal.SIGKILL)
        try:
            while os.waitpid(-1,os.WNOHANG)[0]: pass
        except ChildProcessError: return
        time.sleep(0.01)
    raise ValueError('local process cleanup failed')


def _supervise(connection,args,timeout,cwd):
    process=None;message={'ok':False,'code':'command_failed'}
    def cancel(_signal,_frame): raise KeyboardInterrupt()
    signal.signal(signal.SIGTERM,cancel)
    try:
        # PR_SET_CHILD_SUBREAPER keeps detached Chromium grandchildren owned.
        if ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)!=0:
            raise ValueError('Linux subreaper unavailable')
        with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            process=subprocess.Popen(args,cwd=cwd,stdin=subprocess.DEVNULL,
                stdout=stdout,stderr=stderr,start_new_session=True)
            deadline=time.monotonic()+timeout
            while process.poll() is None:
                if stdout.tell()+stderr.tell()>2*1024*1024: raise ValueError('output limit')
                remaining=deadline-time.monotonic()
                if remaining<=0: raise subprocess.TimeoutExpired(args,timeout)
                try: process.wait(timeout=min(0.1,remaining))
                except subprocess.TimeoutExpired: pass
            if process.returncode: raise ValueError('command failed')
            if stdout.tell()+stderr.tell()>2*1024*1024: raise ValueError('output limit')
            stdout.seek(0);stderr.seek(0)
            message={'ok':True,'stdout':stdout.read().decode('utf8',errors='replace'),
                     'stderr':stderr.read().decode('utf8',errors='replace')}
    except subprocess.TimeoutExpired: message={'ok':False,'code':'timeout'}
    except KeyboardInterrupt: message={'ok':False,'code':'cancelled'}
    except BaseException: message={'ok':False,'code':'command_failed'}
    finally:
        # Further cancellation must not interrupt owned-process cleanup.
        signal.signal(signal.SIGTERM,signal.SIG_IGN)
        signal.signal(signal.SIGINT,signal.SIG_IGN)
        try: _cleanup(process)
        except BaseException: message={'ok':False,'code':'cleanup_failed'}
        try: connection.send(message)
        finally: connection.close()


def run_bounded(args,timeout=60,cwd=None):
    if not hasattr(os,'pidfd_open') or not hasattr(signal,'pidfd_send_signal'):
        raise ValueError('Linux pidfd support required for bounded CPU jobs')
    context=multiprocessing.get_context('fork')
    receive,send=context.Pipe(duplex=False)
    worker=context.Process(target=_supervise,args=(send,args,timeout,cwd))
    worker.start();send.close()
    try:
        if not receive.poll(timeout+8): raise ValueError('CPU supervisor deadline exceeded')
        message=receive.recv()
        if not message['ok']:
            if message['code']=='timeout': raise subprocess.TimeoutExpired(args,timeout)
            if message['code']=='cancelled': raise KeyboardInterrupt()
            raise ValueError('bounded local command failed')
        return {'stdout':message['stdout'],'stderr':message['stderr']}
    finally:
        if worker.is_alive():
            worker.terminate()  # Supervisor handles this and cleans its owned tree.
            worker.join(timeout=6)
        if worker.is_alive():
            worker.kill();worker.join(timeout=1)
        else: worker.join(timeout=1)
        receive.close()
