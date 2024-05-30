
# PPPwn-PS4Browser_not_only

Hello, everyone! I hope you're all doing well. I've been following the scene for years and wondered: how could I assist the great security researchers, PS4 players, developers, and friends?

### Context
In his latest exploit called **'PPPwn', TheOfficialFlow** has allowed us to advance the state of the art of PlayStation jailbreaks, covering firmware versions up to 11.00. I was thrilled about this. However, I noticed that many couldn't use the web browser for exploitation due to the lack of a pre-configured network allowing Ethernet connection, as PPPoE keeps trying to connect.

**So, I asked myself: how could we overcome this challenge?**

I started studying the possibility of triggering the exploit via the native PS4 browser (WWW app). I tried various approaches, which I won't detail here, but one idea worked:

**Using the built-in Wi-Fi hotspot on the PS4, created for remote play via PS VITA or PS TV.**

Great idea, but I couldn't connect to the network. The simple question was: **What's the password?**

**So I started tinkering with the PS4's file system after unlocking it. After three intense weekends, I developed a methodology to discover the password.**

**I was able to connect  a built-in Wi-Fi hotspot WITHOUT PS VITA and use this network to trigger an exploit in the native PS4 browser (WWW app)!!!**


**Note: I won't disclose this part yet because Sony states:
'Give us reasonable time to remediate vulnerabilities before talking about them publicly and notify us of your disclosure plans in advance.'

https://hackerone.com/playstation?type=team#:~:text=Give%20us%20reasonable%20time%20to%20remediate%20vulnerabilities%20before%20talking%20about%20them%20publicly%20and%20notify%20us%20of%20your%20disclosure%20plans%20in%20advance.

So, friends, as soon as Sony responds, I will share with you.

**Please don't insist! I won't disclose until Sony authorizes it.**

### Methodology

#### Step 0 - Discovering the Wi-Fi password

Please wait! Meanwhile, the steps below can help you trigger the vulnerability via browser or curl!

#### Step 1 - Environment Preparation (Installation):

I prepared a Docker setup with everything you need to perform the jailbreak. While waiting for Sony to authorize my report, let's use the browser or curl.

!!!!**IMPORTANT!!! Docker uses port 80 in host mode connected directly interface from host***

You need a system to trigger the exploit, whether it's Windows, Raspberry Pi, or something else, but I believe you need at least the following hardware requirements:

- Router
- Linux OS system (capable of running Docker)
- Wi-Fi Network Card (used to trigger the vulnerability via browser or curl)
- Ethernet Network Card (used to send the exploit data **'PPPwn', TheOfficialFlow**)

It's quite simple; we'll use a Flask application that uses Redis and Celery to execute the exploit and send malicious data to the PS4 via Ethernet.

So all you need is to have Docker Compose installed, and the script will handle the rest. The example below is for a Debian x64 Linux and these are the official requirements:

```sh
sudo apt-get update 
sudo apt-get install -y docker docker-clean docker-compose docker-doc docker-registry docker.io docker2aci
```

Downloading the repository:

```sh
git clone https://github.com/francoataffarel/PPPwn-PS4Browser_not_only.git
cd PPPwn-PS4Browser_not_only
```

First, you need to modify the Ethernet network card that will send the malicious data from **'PPPwn', TheOfficialFlow** in app.py. example:

```sh
sed -i 's/enp1s0/eth0/g' app.py
```

Here’s a complete example of how you would do this:

1. **Start the services, rebuilding the images**:
       
    ```sh
    docker-compose up --build --remove-orphans
    ```
Now you need to connect to the Wi-Fi network that will trigger via browser or curl.

In the example, I'll show triggering via the host itself:

REQUEST: 
```sh
curl -X POST http://localhost/start_exploit
```

RESPONSE: 
```json
{"task_id":"de5dd6a9-21b6-490a-9bf5-cbb67c89112d"}
```

But in the future, as soon as Sony authorizes, it will be directly in the PS4 browser. I promise.

**Please Wait** Exploit will work!

After PPPwed!! You can


2. **Stop and remove the containers and images**: After stopping the containers with `Ctrl + C`, run:

    ```sh
    docker container rm pppwn-ps4browser_not_only_web_1; docker image rm pppwn-ps4browser_not_only_web:latest
    ```

## Interesting Notes

If you think you can help me, please, lend a hand!

I used PPPwn_CPP from **xfangfang**! Thanks, Bro!
https://github.com/xfangfang/PPPwn_cpp/releases/tag/1.0.0

## TO DO

- Display the result in real-time on the browser screen.
- Display the result in real-time in the output of the command execution.
- Create UML diagrams explaining the process.
