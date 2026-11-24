#!/bin/bash
# Run on the rented machine, over ssh, after the job's swarm/ folder has been filled:
#
#     bash ~/jobs/<name>/swarm/start.sh <name>
#
# It lays the job's repos and files out under ~/jobs/<name>/work and starts the job under systemd, as a unit of its
# own (swarm-job-<name>), so that it goes on when this connection is gone. Asked again, it does nothing that is
# already done. It does nothing while another job runs on the machine (code 8): they would share a GPU and a port.
set -euo pipefail
name="$1"
root="$HOME/jobs/$name"
unit="swarm-job-$name"
cd "$root/swarm"
if systemctl is-active --quiet "$unit" 2>/dev/null; then echo "the job is running"; exit 0; fi
if [ -f status.json ] && grep -q '"phase": "finished"' status.json; then echo "the job has finished"; exit 0; fi
busy=$(systemctl list-units --type=service --state=active,activating,deactivating --no-legend --plain 'swarm-job-*' 2>/dev/null | awk '{print $1}' | head -n 1 || true)
if [ -n "$busy" ]; then echo "another job is running on this machine ($busy)" >&2; exit 8; fi
mkdir -p "$root/work" logs
missing=""
for tool in git rsync; do command -v "$tool" >/dev/null || missing="$missing $tool"; done
if [ -n "$missing" ]; then
    sudo apt-get -o DPkg::Lock::Timeout=600 update -q
    # shellcheck disable=SC2086
    sudo DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=600 install -y -q $missing
fi
for bundle in repos/*.bundle; do
    [ -e "$bundle" ] || continue
    repo=$(basename "$bundle" .bundle)
    if [ ! -d "$root/work/$repo/.git" ]; then
        rm -rf "$root/work/$repo.cloning"
        git clone -q "$bundle" "$root/work/$repo.cloning"
        git -C "$root/work/$repo.cloning" checkout -q --detach "$(cat "repos/$repo.commit")"
        if [ -d "$root/work/$repo" ]; then cp -a "$root/work/$repo/." "$root/work/$repo.cloning/"; rm -rf "$root/work/$repo"; fi
        mv "$root/work/$repo.cloning" "$root/work/$repo"
    fi
done
if [ -d files ]; then cp -a files/. "$root/work/"; fi
[ -f started ] || date '+%Y-%m-%d %H:%M:%S' > started
sudo tee "/etc/systemd/system/$unit.service" >/dev/null <<UNIT
[Unit]
Description=swarm job $name (swarm_engine/cloud)
After=network-online.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$root/swarm
ExecStart=/usr/bin/python3 $root/swarm/runner.py $root/swarm/job.json
StandardOutput=append:$root/swarm/logs/runner.log
StandardError=inherit
KillMode=mixed
TimeoutStopSec=300
Restart=no
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload
sudo systemctl enable -q "$unit"
sudo systemctl start "$unit"
echo "the job is started"
