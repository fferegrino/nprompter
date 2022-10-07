# How to use Notion integrations

This guide will show you how to create a Notion integration
and grant them permission to access content in your Notion
workspace.

## Create a Notion integration

Navigate to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) 
and click the *"+ New integration"* button. You will be presented 
with a form like the one below.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-integration.jpg?ik-sdk-version=javascript-1.4.3&updatedAt=1656749806395)

Give it a name you recognise, select a logo if you want (though 
it is not necessary), make sure you give access to the workspace
you will host your content in. As for the capabilities, only 
select "Read content" and "No user information". 
Then click *"Submit →"*.

## Getting an **Integration Token**

Once your integration has been created, you will be presented
with a screen like the one below:

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/secret.png?ik-sdk-version=javascript-1.4.3&updatedAt=1656750179940)

Clicking on *"Show"* will reveal a string starting with *"secret_ ..."* 
this is your **integration token**, save it somewhere safe, you will need it.

## Granting access to your integration

Having an integration token is just the first piece of the puzzle, 
it does not do too much on its own. The next task is to allow your
integration to query data from your Notion workspace.

Navigate to a database (i.e. a board, table or similar page) and click
*"Share"* at the top right corner of the page.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/give-access.png?ik-sdk-version=javascript-1.4.3&updatedAt=1656750179716)

In the box *"Add emails, people, integrations..."* type the name of
the integration you created above. It should appear below for you to select 
and invite.

To make sure you granted it permission, click *"Share"* again, and you
should see something similar to this: 

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/making-sure.png?ik-sdk-version=javascript-1.4.3&updatedAt=1656750180406)

## Identifying your page id

To fetch data from *nprompter*, it is necessary to know in advance which
page to fetch. To identify this, look in the address bar of your browser

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/db-id.png?ik-sdk-version=javascript-1.4.3&updatedAt=1656750180841)

The **database id** is a long string containing alphanumeric characters.
