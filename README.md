# Feed Extension

The Feed extension allows site administrators to include blog entries in the main content of templates using named
references to atom or rss feeds.

**Note: This extension requires ckan 1.7 or higher**

## Activating and Installing

To install the plugin, enter your virtualenv and load the source::

 (pyenv)$ git install -e hg+https://github.com/okfn/ckanext-feedcontent#egg=ckanext-feedcontent

This will also register a plugin entry point, so you now should be
able to add the following to your CKAN .ini file::

 ckan.plugins = feed_content <other-plugins>

**At this point nothing will have happened**! To add feeds to your system see the next section.

## Running the tests

You can run the tests from the root of this repository with the following command

```
nosetests --ckan --with-pylons=test-core.ini ckanext/feedcontent/tests/
```

## Using the Extension

### Adding feeds

To add feeds to CKAN you should log on as a system administrator and then visit /feed/ from where you will be able to add a new feed or edit an existing one.  When you need to update a feed you should visit /feed/ from where you will be able to view the feed to be updated and then press the update button.

### Configuring snippets for presentation

How? 
Using ckan.feeds.default.snippet 

### Using feeds

To reference a feed and an entry in a template ...

