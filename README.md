# Taskman
A PyQT5 Based Task Manager for Linux and MacOS.

## CHANGELOG

### 0.1.0
- View list of active processes and their resource consumption
- Show User processes or All processes
- Send POSIX Signal Interrupts to processes to Terminate, Suspend, etc.
- Supported Signals
  - SIGTERM
  - SIGKILL
  - SIGSTOP
  - SIGCONT
  - SIGINT
  - SIGQUIT
  - SIGTSTP
  - SIGUSR1
  - SIGUSR2
- Can select multiple processes to send signals to.
- Right click on a process to send a signal to it.
- Can sort processes by PID, Name, User, CPU%, Memory%, Command and Status
- Choose between multiple update intervals
  - Normal (1000ms)
  - Slow (5000ms)
  - Realtime (100ms)

## TODO
- Process Manager
  - [X] View list of user processes
  - [X] View list of all processes
  - [X] Sort processes by PID, Name, User, CPU%, Memory%, Command and Status
  - [X] Send POSIX Signals to processes
  - [X] Send signals to multiple processes
  - [ ] Search for processes by name or PID
  - [ ] View process details
  - [ ] View process tree
  - [ ] Launch new processes

- System Monitor
  - [ ] View CPU usage
  - [ ] View GPU usage
  - [ ] View Memory usage
  - [ ] View Disk usage
  - [ ] View Network usage
  - [ ] View Battery information
  - [ ] View System information
  - [ ] View System logs

- Settings
  - [X] Change update interval
  - [ ] Change theme
  - [ ] Change language
  - [ ] Change default signals
  - [ ] Customize columns in process manager



- Other
  - [X] About page
  - [ ] Help page
  - [ ] Add support for MacOS
  - [ ] Add support for Windows (maybe )



## Issues
- Selected process can change when the list is updated (workaround: use No Update interval)




