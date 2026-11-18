# Administrative task reference

The automated demo uses a temporary Linux workspace and a loopback HTTP server. The original assignment also includes root, package-management and SSH lifecycle exercises. Perform the following only in the intended disposable course VM with console access. This reference records the commands; the saved automated result does not claim they were executed.

## Identity and root session

Run whoami and id before and after sudo -i. Use exit to return to the regular account. A prompt character can be customized, so id -u provides a stronger check than the prompt appearance.

## Package management

    sudo apt update
    sudo apt upgrade
    sudo apt install tree wget curl xxd openssh-server
    tree --version
    wget --version

Review package changes interactively. The maintained lab uses Ubuntu/WSL for the repeatable exercises; the original brief describes a Kali virtual machine.

## SSH lifecycle

    systemctl status ssh.service
    sudo systemctl start ssh.service
    sudo systemctl stop ssh.service
    sudo systemctl restart ssh.service
    sudo systemctl enable ssh.service
    sudo systemctl disable ssh.service
    systemctl list-units --all 'ssh*'
    systemctl list-unit-files 'ssh*'

Service names and socket activation vary by distribution. Inspect ssh.socket as well as ssh.service where present. Enabling a unit configures boot activation; start controls the current running state.

## Configuration validation

Back up the intended configuration and validate a candidate before applying it. Keep console access available when changing SSH.

    sudo /usr/sbin/sshd -t -f /etc/ssh/sshd_config
    sudo systemctl reload ssh.service
    journalctl -u ssh.service --since '10 minutes ago'

The assignment asks for an intentional failure. A candidate file containing an unsupported option can be checked with sshd -t -f before restoring the valid file. A syntax-check result should identify the relevant line. Restoring configuration and validating it are required before any service restart. This project has not modified the host SSH service.

## Locate and find

A locate index can lag behind current files. Where installed, update its index using the documented distribution procedure, then compare locate grep_task.txt with find in the course workspace. The automated demo uses find within its fixture directory.

References

- [systemctl manual](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)
- [OpenSSH sshd manual](https://man.openbsd.org/sshd)
