# How to use Notion integrations

This guide will show you how to create a Notion integration and grant them permission to access content in your Notion workspace.

## Create a Notion integration

Navigate to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) and click the *"+ New integration"* button. You will be presented  with a form like the one below.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-integration.jpg?ik-sdk-version=javascript-1.4.3&updatedAt=1656749806395)

Give it a name you recognise, select a logo if you want (though it is not necessary), make sure you give access to the workspace you will host your content in. As for the capabilities, only  select "Read content" and "No user information". Then click *"Submit →"*.

## Getting an **Integration Token**

Once your integration has been created, you will be presented with a screen like the one below:

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/secret.png?ik-sdk-version=javascript-1.4.3&updatedAt=1656750179940)

Clicking on *"Show"* will reveal a string starting with *"secret_ ..."* this is your **integration token**, save it somewhere safe, you will need it to use _Nprompter_.

## Granting access to your integration

Having an integration token is just the first piece of the puzzle, it does not do too much on its own. The next task is to allow your integration to query data from your Notion's database.

Navigate to a database (i.e. a board, table or similar page) and click on the three dots in the top right corner of the page, then select the option _Add connections_, and in the window that opens search for your integration, in my case, it is the _My teleprompter_.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/share-page-new-integration.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665261016749)

It will ask for your confirmation before granting access to the database and any subpage under it.

## Identifying your page id

To fetch data from *Nprompter*, it is necessary to know in advance which page to fetch. To identify this, look in the address bar of your browser for a long alphanumeric string

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/db-id.png?ik-sdk-version=javascript-1.4.3&updatedAt=1656750180841)

This is the necessary information you will need to use _Nprompter_, now you can [check its usage](./usage.md).
