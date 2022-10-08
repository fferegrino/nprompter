Using Nprompter
===============

## `build`

This command is used to generate your teleprompter pages from a Notion database.

After you have [created an integration](./create-integration.md), and  the next step is as easy as running the command `build`:

```shell
nprompter build [DATABASE ID] (NOTION_API_KEY)
```

This command will generate a bunch of html files in a folder named `prompter`, just open the `index.html` file inside that browser to start using your teleprompter.

 > Note that you can specify the `NOTION_API_KEY` parameter via a environment variable too, and it is arguably a better alternative.

## Options

The build command takes several *optional* parameters that allow for great customisation:

 * `-o [PATH]` / `--output [PATH]`: to specify where the output should be written to. Defaults to *"./prompter"*.  
 * `-f [STRING]` / `--filter [STRING]`: Nprompter fetches data from a Notion database filtering by properties and specific values, use this to specify which property to filter by. Defaults to *"Status"*.
 * `-v [STRING]` / `--value [STRING]`: Nprompter fetches data from a Notion database filtering by properties and specific values, use this to specify which value to search for. Defaults to *"Ready"*.
 * `-c [PATH]` / `--config [PATH]`: Specifies the location of a configuration file. Defaults to *None*.
 * `-s [PATH]` / `--extra-css [PATH]`: Specifies the location of an additional CSS file to further customize the teleprompter's appereance. Defaults to *None*.  
 * `--download/--no-download`: A flag that specifies whether to download information from _Notion_ or simply regenerate the styles that accompany the teleprompter. Defaults to *--download*.

