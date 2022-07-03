nprompter
=========

A Notion backed web teleprompter

## Installation  

```bash
pip install nprompter
```

## Usage

You will need a Notion *integration token* as well as a database id.
To learn how to get these, check the [create-integration.md](create-integration.md)
page.

After, set the integration token as value for the `NOTION_API_KEY` environment variable.

```bash
export NOTION_API_KEY="secret_xMXNQ7mw2IMc... (replace it with yours)"
```

Say you have a board like this: [Example board](https://nprompter.notion.site/c68ccc052d1b4eaaa3091e637f7011c0?v=5435599e709e48d8b23c4471ae8102a5)
with id `c68ccc052d1b4eaaa3091e637f7011c0`, to download the content
it is necessary to run:

```bash
nprompter build c68ccc052d1b4eaaa3091e637f7011c0
```

Note that all the pages you want to download from your database should contain a *"Status"* property with its value 
set to *"Ready"*. You can modify the name of the property or its value with the arguments `--property-filter` and 
`--property-value` of the `nprompter build` command. 

Then, to launch a local webserver, run:

```bash
nprompter serve
```

## Demo and deploying to the cloud

You can have your teleprompter at the ready by deploying it to the cloud, using a provider such as **Netlify**,
check the files under *[deploy_examples](deploy_examples)*. For example see how, [this board]((https://nprompter.notion.site/c68ccc052d1b4eaaa3091e637f7011c0?v=5435599e709e48d8b23c4471ae8102a5))
looks like when deployed automatically to [https://nprompter.netlify.app/](https://nprompter.netlify.app/).
