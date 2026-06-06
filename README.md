# webserv_tester

## Installation & Set Up

### Step 1: Clone in the right location
Clone the webserv_tester repository into the root directory of your webserv project folder. The tester assumes that a ./webserv exectuable will also exist in this root.


```
cd webserv
git clone git@github.com:h-allison/webserv_tester.git
```
```
.
└── /webserv <-- project directory/
    ├── webserv <-- executable
    └── /webserv_tester <-- tester repository
```

You will probably want to add the webserv_tester repository to your webserv's .gitignore.

### Step 2: Configure the Config Files

In the webserv_tester directory, run

```
./config.sh
```

What this is for: webserv_tester includes test config files (as well as test websites) for webserv to use. The config files themselves must be configured to contain the correct paths to the test websites, based on your file system.

## Run:

The webserv_tester executable is located at:

./webserv_tester/tests/main.py

You can of course add an alias to this path in your .zshrc, in order to run the tester from any other location.

## Common Issues & Their Solutions

Common Problem #1:
```
webserv failed to start with config ...
```

This is almost always caused by webserv still running in other process, or another server using the same port. First check that you don't have webserv running in another window. If you can't find it, there's still a good chance it might still be a runaway process, due to the tester exiting unexpectedly. Find the PID of another webserv instance with "ps aux | grep webserv" and kill it.


Common Problem #2:

Log file says
```
[ERROR] bind:
```
The exact same thing as above.


