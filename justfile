distro := `grep -oP '^ID=\K.*' /etc/os-release`

[linux]
setup:
    @just _setup_{{distro}}

_setup_arch:
    pacman -Q cdrtools pigz uv || sudo pacman -Sy --noconfirm --color=always cdrtools pigz uv

_setup_ubuntu:
    dpkg -l mkisofs pigz || sudo apt-get install mkisofs pigz
    snap list astral-uv >/dev/null || (sudo snap refresh && sudo snap install --classic astral-uv)

[macos]
setup:
    brew ls --versions cdrtools pigz uv || brew install cdrtools pigz uv

sync:
    uv sync
    uv run -m ansible galaxy role install -r requirements.yml -p roles
    uv run -m ansible galaxy collection install -r requirements.yml -p collections

[group("image")]
[doc("Windows Server 2012")]
windows2012: setup sync
    uv run -m ansible playbook main.yml --limit '*2012'

[group("image")]
[doc("Windows Server 2012 R2")]
windows2012r2: setup sync
    uv run -m ansible playbook main.yml --limit '*2012r2'

[group("image")]
[doc("Windows Server 2016")]
windows2016: setup sync
    uv run -m ansible playbook main.yml --limit '*2016'

[group("image")]
[doc("Windows Server 2019")]
windows2019: setup sync
    uv run -m ansible playbook main.yml --limit '*2019'

[group("image")]
[doc("Windows Server 2022")]
windows2022: setup sync
    uv run -m ansible playbook main.yml --limit '*2022'
