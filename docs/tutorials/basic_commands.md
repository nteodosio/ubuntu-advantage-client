# Getting Started with Ubuntu Pro Client

The Ubuntu Pro Client (`pro`) provides users with a simple mechanism to
view, enable, and disable offerings from Canonical on their system. In this tutorial
we will cover the base `pro` commands that allow a user to successfully manage the offering
on their machine.

## Prerequisites

On this tutorial, you will use [LXD](https://linuxcontainers.org/lxd/) containers.
To set up LXD on your computer, please follow this [guide](https://linuxcontainers.org/lxd/getting-started-cli/).

```{tip}
When configuring LXD on your machine, run the `lxd init --minimal`. This should be more
than enough for you to finish this tutorial
```

## Main `pro` commands

When dealing with `pro` through the CLI, there are six main `pro` commands that cover the main
functionalites of the tool. They are:

* **status**
* **attach**
* **refresh**
* **detach**
* **enable**
* **disable**

In this tutorial, we will go through all those commands to show how to properly use them.
To achieve that, we will use a Xenial LXD container.

## Creating the Xenial LXD container

To test all of those commands, let's create a Xenial LXD container. Remember to set up LXD as
mentioned on the [Prerequisites](#prerequisites) section. After that, just run the command:

```console
$ lxc launch ubuntu-daily:xenial dev-x
```

After running that, let's access the container by running:

```console
$ lxc shell dev-x
```

## Base `pro` commands

### Status

The status command of `pro` allows you to see the status of any Ubuntu Pro service on your machine.
It also easily allows you to verify if your machine is attached to an Ubuntu Pro subscription
or not.

Let's run it on the LXD container:

```console
$ pro status
```

It is expected for you to see an output similar to this one:

```
SERVICE       AVAILABLE  DESCRIPTION
cis           yes        Center for Internet Security Audit Tools
esm-infra     yes        Expanded Security Maintenance for Infrastructure
fips          yes        NIST-certified core packages
fips-updates  yes        NIST-certified core packages with priority security updates
livepatch     yes        Canonical Livepatch service

This machine is not attached to an Ubuntu Pro subscription.
See https://ubuntu.com/pro
```

You can see that the status command shows the services that are available for that given machine,
while also presenting a short description for each of them.

Additionally, if you look at the last lines of the output, you can identify that this machine is not
attached to an Ubuntu Pro subscription.
```
This machine is not attached to an Ubuntu Pro subscription.
See https://ubuntu.com/pro
```

### Attach

To access any of those service offerings, you need to attach to an Ubuntu Pro subscription. This is
achieved by running the attach command. Before you run it, you need to get an Ubuntu Pro token.
Any user with a Ubuntu One account is entitled to a free personal token to use with Ubuntu Pro.
You can retrieve your Ubuntu Pro token from the [Ubuntu Pro portal](https://ubuntu.com/pro/).
You will log in with your SSO credentials, the same credentials you use for https://login.ubuntu.com.
After getting your Ubuntu Pro token, go to the LXD container and run:

```console
$ sudo pro attach YOUR_TOKEN
```

It is expected for you to see an output similar to this one:

```
Enabling default service esm-infra
Updating package lists
Ubuntu Pro: ESM Infra enabled
This machine is now attached to 'USER ACCOUNT'

SERVICE       ENTITLED  STATUS    DESCRIPTION
cis           yes       disabled  Center for Internet Security Audit Tools
esm-infra     yes       enabled   Expanded Security Maintenance for Infrastructure
fips          yes       n/a       NIST-certified core packages
fips-updates  yes       n/a       NIST-certified core packages with priority security updates
livepatch     yes       n/a       Canonical Livepatch service

NOTICES
Operation in progress: pro attach

Enable services with: pro enable <service>

                Account: USER ACCOUNT
           Subscription: USER SUBSCRIPTION
            Valid until: 9999-12-31 00:00:00+00:00
Technical support level: essential
```

From this output, you can see that the attach command enables all of the services specified by the user subscription.
After the command ends, `pro` displays the new state of the machine.
That status output is exactly what you will see if you run the status command again.
You can confirm this by running:

```console
$ pro status
```

One question that may arise is that the output of `pro status` while attached is different from
the output of `pro status` when unattached. When attached, status presents two new columns,
**ENTITLED** and **STATUS**, while also dropping the **AVAILABLE** column. For more information
of why the output is different, please refer to this [explanation](../explanations/status_columns.md).

Finally, another useful bit at the end of both attach and status is the contract expiration date:

```
    Account: USER ACCOUNT
Subscription: USER SUBSCRIPTION
Valid until: 9999-12-31 00:00:00+00:00
```

The `Valid until` field describes when your contract will be expired, so you can be aware of when it
needs to be renewed.


### Refresh

In the last section, we mentioned that your contract can expire. Although free tokens never expire, if
you buy an Ubuntu Pro subscription, and later need to renew the contract, how you can make your machine aware of
it? You can do this through the `refresh` command:

```console
$ sudo pro refresh
```

This command will refresh the contract on your machine. This command is also really useful if you
want to change any definitions on your subscription. For example, let's assume that you now want
`cis` to be enabled by default when attaching. After you modify your subscription for that, running
the refresh command will process any changes that were performed in the subscription, enabling
`cis` because of this.

```{seealso}
The refresh command does more than just update the contract in the machine. If you want
more information about the command, please take a look at this [explanation](../explanations/what_refresh_does.md).
```

### Enable

There is another way to enable a service that wasn't activated during attach or refresh.
Suppose that you want to enable `cis` on this machine manually. To achieve that, You can use the
enable command.

Let's enable `cis` on our LXD container by running:

```console
$ sudo pro enable cis
```

After running it, you should see an output similar to this one:

```
One moment, checking your subscription first
Updating package lists
Installing CIS Audit packages
CIS Audit enabled
Visit https://security-certs.docs.ubuntu.com/en/cis to learn how to use CIS
```

You can confirm that `cis` is enabled now by running:

```console
$ pro status
```

And you should see:
```
SERVICE       ENTITLED  STATUS    DESCRIPTION
cis           yes       enabled   Center for Internet Security Audit Tools
esm-infra     yes       enabled   Expanded Security Maintenance for Infrastructure
fips          yes       n/a       NIST-certified core packages
fips-updates  yes       n/a       NIST-certified core packages with priority security updates
livepatch     yes       n/a       Canonical Livepatch service
```

You can see now that `cis` is marked as `enabled` on status.


### Disable

Let's suppose that you don't want a service anymore, you can also disable any service offering
through `pro`. For example, let's disable the `cis` service you just enabled by running on the LXD
container:

```console
$ sudo pro disable cis
```

After running that command, let's now run `pro status` to see what happened to `cis`:
```
SERVICE       ENTITLED  STATUS    DESCRIPTION
cis           yes       disabled  Center for Internet Security Audit Tools
esm-infra     yes       enabled   Expanded Security Maintenance for Infrastructure
fips          yes       n/a       NIST-certified core packages
fips-updates  yes       n/a       NIST-certified core packages with priority security updates
livepatch     yes       n/a       Canonical Livepatch service
```

You can see that `cis` status is back to disabled.

```{note}
The disable command doesn't uninstall any package that was installed by
the service. The command only removes the access you have to the service, but it
doesn't undo any configuration that was applied on the machine.
```

### Detach

Finally, what if you don't want this machine to be attached to an Ubuntu Pro subscription any longer?
You can achieve that using the `detach` command:

```console
$ sudo pro detach
```

This command will disable all of the Ubuntu Pro services on the machine for you and
get rid of the subscription stored on your machine during attach.

```{note}
The detach command will also not uninstall any packages that were installed by
any service enabled through `pro`.
```

### Final thoughts

This tutorial has covered the 6 main commands of `pro`. If you need more advanced options to configure
the tool, please take a look at the _How To Guides_. If that still doesn't cover
your needs, feel free to reach the `pro` team on `#ubuntu-server` on Libera IRC.

Before you finish this tutorial, exit the container by running `CTRL-D` and delete it by running
this command on the machine:
```console
$ lxc delete --force dev-x
```
