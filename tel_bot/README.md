# what is this?
its a telegram bot for our front-end developer to be able to manually update<br />
the server without any problems

## alternatives
**i know that using pipelines and ansible is the standard way**<br />
but i try to implement such things to have a template for other usages<br />
so dont worry about it

please add the username and password for server update<br />
and telegram bot api to your env variables

## change sudoers like this

%zerobits01 ALL=(ALL) NOPASSWD: /bin/systemctl restart kit365-ui.service<br />
%zerobits01 ALL=(ALL) NOPASSWD: /bin/systemctl reload kit365-ui.service<br />
%zerobits01 ALL=(ALL) NOPASSWD: /bin/systemctl reload kit365-api.service<br />
%zerobits01 ALL=(ALL) NOPASSWD: /bin/systemctl restart kit365-api.service<br />
