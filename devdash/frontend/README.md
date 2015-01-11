# Getting started

## Requirements

- [npm](https://npmjs.org/)
- [grunt-cli](http://gruntjs.com/getting-started)
- That's it! NPM will help you install everything else you need.

## Workflow

1. `npm install`
  – Initializes Grunt in this folder and installs dependencies.
- `grunt vendor`
  1. Installs Bower components.
  - Runs `grunt bower:install` which does a number of things:
    - Installs the Bower dependencies.
    - Moves all Bower dependencies to `vendor`.
      - If a `main` property is set on the dependency then that is the only file
        that will be carried over.
      - If image or font assets of a dependency are listed in the `exportsOverride`
        section of `bower.json` then those assets are sent to the `src/static/img`
        or `src/static/fonts` folders respecitvely.
        All other assets listed in the `exportsOverride` section of `bower.json`
        will end up in a `vender/DEPENDENCY-NAME` folder. NO other files will be
        carried over so be careful.
        This is helpful because it allows you to really slim down the dependency
        folder to the bare minimum of what you need.
  - Concatenates all Capital Framework Less files to `vendor/cf-concat/cf-concat.less`
    to make importing them easier.
- `grunt vendor-to-static`
  - Copies Bower dependencies to `src/static` if specified in the `cop:vendor`
    task options. This is useful for dependency files that you don't want to
    concatenate into your CSS or JS files but need to be referenced individually.
- `grunt cssdev`
  – Compiles `main.less` to `main.css`
  - Runs autoprefixer on `main.css` (so please don't use vendor prefixes in your
    styles)
  - Minifies `main.css` to `main.min.css`
  - Adds a banner to `main.min.css`
- `grunt jsdev`
  - Concatenates all JavaScript files specified in the `concat:bodyScripts` task
    options into `main.js`.
  - Minifies `main.js` to `main.min.js`.
  - Adds a banner to `main.min.js`
- `grunt` - The default Grunt task runs both `grunt cssdev` and `grunt jsdev` as well
  as `shell:manage_py`, which is needed to copy files from the `devdash/frontend/dest`
  to `devdash/static/`.
- `grunt watch`
  - In an effort to minimize the amount of time waiting for grunt tasks to run while
    developing, `grunt watch` has been split into several sub tasks. Running `grunt watch`
    will run all of these sub tasks and will run only the tasks that are needed. Just
    remember that while using `grunt watch` you should be careful about modifiying files
    before the grunt task completes, or else it might not detect the change.


