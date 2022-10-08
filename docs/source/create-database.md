# Creating a new Notion database

Though _Nprompter_ works with your already existing databases, this guide will walk you through the creation of a completely new database that will work out of the box.

## Add a page

On the left hand side of your Notion home screen you will see a list of all your pages and an option to add a new one. Click there to begin.

![Add a page screen](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-add-page.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665220938460)

## Customise page

Set a page name, icon, header image or any other customisation you want. Then, under the _DATABASE_ section select _Board_:

![Customise page](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-board.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665220939151)

 > 🤔 _Nprompter_ should work with any database, but a board is a nice way to organise scripts

## Create a new database

After clicking _Board_ in the previous screen, on the right hand side of your screen you will be prompted to select a data source. Select _New database_ to create a new database.

![New database](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-new-database.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665220938835)

After creating a new database, you will see something like this, a default semi-empty database with three pages sitting in the _To-do_ column.

![Default database](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-full-board.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665220939063)

Click on one of the cards to bring up the full details of the page, we need to make some changes in there.

## Change page's properties

Once you click on the card you will be able to see it, along with its details. In the new page, click on the _Status_ property and then select _Edit property_.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-edit-property.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665220938561)

 > Notion [has introduced](https://www.notion.so/help/guides/status-property-gives-clarity-on-tasks) a new property of type "Status", _Nprompter_ currently only works using a property of this type. 

Modify this property as you wish, for example I have edited the values of the property to look like this:

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-edited.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665221738264)

As you can see, I have statuses for scripts that are just an _Idea_, for the moment I start _Writing_ them, when they're _Ready_ and when I have _Recorded_ them.

## Change grouping

If you visit your board's page you will notice that your changes are not yet visible; You still have three columns: To-Do, In progress and Complete. To reflect the changes you made to the _Satus_ property, you will need to change the grouping. Click on the three dots at the top right of your board and then click on _Group_.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-change-group.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665221737035)

Then change the value of _Sort by_ from _Group_ to _Option_.

![](https://ik.imagekit.io/thatcsharpguy/posts/nprompter/create-page-change-group-to-option.png?ik-sdk-version=javascript-1.4.3&updatedAt=1665221736262)

 > 😬 As of the writing of this documentation there is no way to rearrange the columns. So if yours are out of order, do not worry. Hopefully Notion will do something for us soon.

And that is it! you have created your first page fully compatible with _Nprompter_. The next thing you need to do is [create an integration](./create-integration.md).
