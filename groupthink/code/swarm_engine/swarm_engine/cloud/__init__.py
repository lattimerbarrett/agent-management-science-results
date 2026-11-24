"""Rent a GPU for one job: wait for one to be free, set it up, run the job, bring back what it made, give it back.

    lambda_api.py     Lambda's cloud API: what is free, launch, look, terminate
    job.py            what a job is (what to rent, what to send, what to run, what to bring back) and where it stands
    controller.py     takes a job from "wanted" to "given back", a step at a time, and can be stopped and started
                      again at any point; `python3 -m swarm_engine.cloud` is its command line
    remote/           what runs on the rented machine: it sets itself up, runs the job's commands and says how far it is

Three machines are involved, and the split between them is what makes a job safe to walk away from:

    where a job is handed in   a laptop. It packs the job, hands it to the controller's machine, and can be closed.
    the controller's machine   one that is always on (a home server). It holds the API key, waits for a GPU to be
                               free, launches it, copies the job's results off it every minute, and terminates it
                               when the job has ended and everything is copied. A job is a folder there; a line in
                               its crontab starts the controller again if the machine was restarted.
    the rented machine         runs the job under systemd, so nothing depends on a connection staying up. It holds
                               no key: it cannot rent or terminate anything, and what it made is copied off it by
                               the controller's machine, which reaches it over ssh.

Lambda bills a machine until it is terminated through the API (a shutdown from inside it does not stop that), so
a job is never left in a state where nothing will terminate its machine: see `Controller` for the rules.

Nothing here needs more than Python's standard library, ssh and rsync: the controller runs on a machine that has
none of this repo's environment.
"""
