These are some notes about how to use this code.

## The form & settings

Create a Google form and save the results to a sheet. The required columns are
`Opt in` (where `Yes` means that this user will be included) and `Email
Address`. You should also create a second page on that sheet called something
like `Previous`.

You'll need your Google "service account" credentials stored as JSON in a file.
You should share editing permissions with for the sheet with this account.

Then take a look at `settings/config.yaml.template` for all the required
settings. These settings should then be saved as
`sites/name_of_site/config.yaml`.

## Docker

To build the Docker image, run:

```bash
docker build --tag flatiron-coffee .
```

Then for a dry run, execute:

```bash
docker run --rm -it -v $(pwd)/sites:/app/sites -v $(pwd)/settings:/app/settings flatiron-coffee name_of_site
```

To actually send the emails:

```bash
docker run --rm -it -v $(pwd)/sites:/app/sites -v $(pwd)/settings:/app/settings flatiron-coffee name_of_site --send
```
